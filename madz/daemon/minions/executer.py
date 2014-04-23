import sys
import os
import threading
import queue
import time
import subprocess
import logging
import traceback

logger = logging.getLogger(__name__)

import zmq

from .IMinion import IMinion
from ..Daemon import Daemon
from ...config import *

# from: http://stackoverflow.com/questions/2554514/asynchronous-subprocess-on-windows
def simple_io_thread(pipe, queue, tag, stop_event):
    """
    Read line-by-line from pipe, writing (tag, line) to the
    queue. Also checks for a stop_event to give up before
    the end of the stream.
    """
    while True:
        line = os.read(pipe.fileno(), 1024)

        while True:
            try:
                # Post to the queue with a large timeout in case the
                # queue is full.
                queue.put((tag, line), block=True, timeout=0.1)
                break
            except Queue.Full:
                if stop_event.isSet():
                    break
                continue
        if stop_event.isSet():
            queue.put((tag, ""), block=True)
            break
        
        if len(line) == 0:
            break

class ExecuteStreamSpitterThread(threading.Thread):
    def __init__(self, subproc_control):
        super().__init__()
        self._control = subproc_control

        # Build networking, should probably be done on thread with an event
        self.context = zmq.Context()
        self.stdin = self.context.socket(zmq.SUB)
        self.stdout = self.context.socket(zmq.PUB)
        self.stderr = self.context.socket(zmq.PUB)

        self.stdin.setsockopt(zmq.SUBSCRIBE, b'')

        bind_fmt = "tcp://127.0.0.1:{port}"
        self.stdin.bind(bind_fmt.format(port=self._control.stdin_port))
        self.stdout.bind(bind_fmt.format(port=self._control.stdout_port))
        self.stderr.bind(bind_fmt.format(port=self._control.stderr_port))

    def run(self):
        # Build async subproc communication threads
        commqueue = queue.Queue()
        stop_event = threading.Event()

        procin = self._control.subproc.stdin
        procout = self._control.subproc.stdout
        procerr = self._control.subproc.stderr

        if (procin is None) or (procout is None) or (procerr is None):
            self.stdout.send_pyobj("")
            self.stderr.send_pyobj("")
            self.stdin.close()
            self.stdout.close()
            self.stderr.close()
            return

        stderr_thread = threading.Thread(
            target=simple_io_thread,
            args=(procerr, commqueue, "STDERR", stop_event)
        )
        stdout_thread = threading.Thread(
            target=simple_io_thread,
            args=(procout, commqueue, "STDOUT", stop_event)
        )

        stderr_thread.daemon = True
        stdout_thread.daemon = True

        stderr_thread.start()
        stdout_thread.start()

        # Main loop
        exiting = False
        joined = False
        empty = False
        while True:
            # Forward output
            try:
                tag, line = commqueue.get(False)
                if tag == "STDOUT":
                    self.stdout.send_pyobj(line)
                elif tag == "STDERR":
                    self.stderr.send_pyobj(line)
            except queue.Empty:
                empty = True

            # Forward input
            if not joined:
                try:
                    inp = self.stdin.recv_pyobj(zmq.NOBLOCK)
                    procin.write(inp)
                    procin.flush()
                except zmq.ZMQError:
                    pass
            # Check subproc not finished finished
            if (not (self._control.subproc.returncode is None)) \
                or self._control._minion.banished:
                exiting = True

            # If the subproc is finished we need to join, and then empty the queue
            if exiting:
                if not joined:
                    stop_event.set()
                    self.stdin.close()
                    procin.close()

                    stderr_thread.join()
                    stdout_thread.join()

                    procout.close()
                    procerr.close()

                    joined = True
                    empty = False
                # We have finished, we can exit now:
                elif empty:
                    break;

        self.stdout.close()
        self.stderr.close()
        self.context.term()


class ExecuterMinionSubprocess(object):
    class ControlThread(threading.Thread):
        def __init__(self, control):
            super().__init__()
            self._control = control

        def run(self):
            while True:
                if hasattr(self._control, "subproc") and not (self._control.subproc.poll() is None):
                    break;
                if self._control._minion.banished:
                    self._control.subproc.kill()
                    break;
            # clean up

    def __init__(self, minion):
        self._minion = minion._minion

        self.bootstrap_port = Daemon.next_minion_port()
        self.control_port = Daemon.next_minion_port()
        self.stdin_port = Daemon.next_minion_port()
        self.stdout_port = Daemon.next_minion_port()
        self.stderr_port = Daemon.next_minion_port()

        self._bind_str = "tcp://127.0.0.1:{port}".format(port=self.bootstrap_port)
        self._proc_bootstrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "executer_bootstrap.py"))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind(self._bind_str)

        self._spitter = ExecuteStreamSpitterThread(self)
        self._thread = ExecuterMinionSubprocess.ControlThread(self)
        self._thread.start()


    def banish(self):
        self._thread.join()
        if self._spitter.isAlive():
            self._spitter.join()


    def execute(self, argv, userconfig):
        system = Daemon.current.system

        subproc_sys_args = {
            "stdin": subprocess.PIPE,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE
        }
        if os.name == "nt":
           subproc_sys_args["creationflags"] = subprocess.CREATE_NEW_CONSOLE
           del subproc_sys_args["stdin"]
           del subproc_sys_args["stdout"]
           del subproc_sys_args["stderr"]

        # Start subprocess
        self.subproc = subprocess.Popen(
            [sys.executable, self._proc_bootstrapper, os.path.dirname(self._proc_bootstrapper), self._bind_str],
            cwd=os.getcwd(),
            bufsize=1,
            **subproc_sys_args)

        self._spitter.start()

        with config.and_merge(system.config):
            with config.and_merge(userconfig):
                system.index()

                execute_plugin_name = argv[0] if len(argv) > 0 else config.get(OptionSystemExecutePlugin)
                execute_function_name = argv[1] if len(argv) > 1 else config.get(OptionSystemExecuteFunctionName)

                if execute_plugin_name is None:
                    logger.error("DAEMON[{}] cannot execute. OptionSystemExecutePlugin is not defined.".format(self._minion.identity()))
                    return

                plugin_stub = system.resolve_plugin(execute_plugin_name)

                if(plugin_stub.executable == False):
                    logger.error("DAEMON[{}] cannot execute {}. executable flag not set to True.".format(self._minion.identity(), plugin_stub.id.namespace))
                    return

                logger.debug("DAEMON[{}] Loading plugins for '{}' targeting function '{}'.".format(
                        self._minion.identity(),
                        execute_plugin_name,
                        execute_function_name
                    ))
                self.load(plugin_stub)

                logger.info("DAEMON[{}] Calling function '{}' from plugin '{}'.".format(self._minion.identity(), execute_function_name, execute_plugin_name))
                self.call_func(plugin_stub, execute_function_name)

                logger.info("DAEMON[{}] Completed, new instance started!".format(self._minion.identity()))


    @staticmethod
    def _unique(seq):
        seen = set()
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            yield x

    @staticmethod
    def _gen_load_pattern(plugin_stub, until="final"):
        # base:
        res = []

        # get into memory:
        res += [("in-mem", plugin_stub, [])]
        if until == "in-mem":
            return res

        # init:
        depends = plugin_stub.gen_recursive_loaded_depends()
        res += [load_pattern for require in depends for load_pattern in ExecuterMinionSubprocess._gen_load_pattern(require, "inited")]
        res += [("inited", plugin_stub, depends)]
        if until == "inited":
            return res

        # final
        imports = list(filter(lambda p: p not in depends, plugin_stub.gen_required_loaded_imports()))
        res += [load_pattern for require in imports for load_pattern in ExecuterMinionSubprocess._gen_load_pattern(require, "final")]
        res += [("final", plugin_stub, imports)]
        if until == "final":
            return res

    def load(self, plugin_stub):
        for p in ExecuterMinionSubprocess._unique(
            map(lambda e: (
                    "load-artifact", 
                    e[0], 
                    str(e[1].output_file_location()), 
                    tuple(map(lambda p: str(p.output_file_location()), e[2]))),
                ExecuterMinionSubprocess._gen_load_pattern(plugin_stub))):
            # Cleanup object for sending:
            sending = p

            while True:
                try:
                    self.socket.send_pyobj(sending, zmq.NOBLOCK)
                    break
                except zmq.ZMQError:
                    if self._minion.banished:
                        raise Exception()
                    continue

            while True:
                try:
                    res = self.socket.recv_pyobj(zmq.NOBLOCK)
                    break
                except zmq.ZMQError:
                    if self._minion.banished:
                        raise Exception()
                    continue

            # Executer responded with traceback
            if (isinstance(res, str)):
                logger.error("DAEMON[{}] Encountered problem loading {}:\n\t{}".format(self.identity(), plugin_stub, res))
                raise Exception("Encountered problem loading {}!".format(plugin_stub))


    def call_func(self, plugin_stub, func):
        index = plugin_stub.get_function_index(func)
        self.socket.send_pyobj(("execute", str(plugin_stub.output_file_location()), index))

        self.socket.close()
        self.context.term()



class ExecuterMinion(IMinion):
    current = None

    class ExecuteControlThread(threading.Thread):
        def __init__(self, minion):
            super().__init__()
            self._minion = minion

        def run(self):
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://127.0.0.1:{port}".format(port=self._minion.port))
            while not self._minion.banished:
                try:
                    command = socket.recv_pyobj(zmq.NOBLOCK)
                except zmq.ZMQError:
                    time.sleep(0.1)
                    continue
                report = None
                try:
                    #TODO: set up logging report
                    logger.info("DAEMON[{}] Starting execute of '{}'.".format(self._minion.identity(), " ".join(command[0])))
                    
                    subproc = ExecuterMinionSubprocess(self)
                    self._minion.subprocs.append(subproc)

                    report = (subproc.stdin_port, subproc.stdout_port, subproc.stderr_port)
                    socket.send_pyobj(report)

                    time.sleep(0.01)

                    subproc.execute(*command)
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on execute of '{}':\n\t{}".format(self._minion.identity(), " ".join(command[0]), tb_string))

    def __init__(self):
        self.banished = False
        self.spawned = False
        self.subprocs = []
        self._thread = ExecuterMinion.ExecuteControlThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def spawn(cls):
        if (cls.current is None):
            cls.current = ExecuterMinion()
        return cls.current._spawn()

    def _spawn(self):
        if not (self.spawned):
            self.spawned = True
            self._thread.start()
        return (self, [self.port])

    def banish(self):
        self.banished = True
        for subproc in self.subprocs:
            subproc.banish()
        self._thread.join()

    @classmethod
    def identity(cls):
        return "executer"

