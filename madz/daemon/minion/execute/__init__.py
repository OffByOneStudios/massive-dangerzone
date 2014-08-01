"""madz/daemon/minion/executer/__init__.py
@OffbyOne Studios 2014
Executer minion.
"""

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

from madz.bootstrap import *
from madz.daemon.minion.core import IMinion
from madz.daemon.core import Daemon

from madz.config import *

class ExecuterMinionSubprocess(object):

    def __init__(self, minion):
        self._minion = minion._minion

        self.bootstrap_port = Daemon.next_minion_port()
        self.control_port = Daemon.next_minion_port()

        self._bind_str = "tcp://127.0.0.1:{port}".format(port=self.bootstrap_port)
        self._proc_bootstrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "executer_bootstrap.py"))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.RCVTIMEO = 200
        self.socket.SNDTIMEO = 200
        self.socket.bind(self._bind_str)

    def banish(self):
        pass

    def execute(self, argv, userconfig):
        system = Daemon.current.system

        with config.and_merge(system.config):
            with config.and_merge(userconfig):
                system.index()

                execute_plugin_name = argv[0] if len(argv) > 0 else config.get(OptionSystemExecutePlugin)
                execute_function_name = argv[1] if len(argv) > 1 else config.get(OptionSystemExecuteFunctionName)

                if execute_plugin_name is None:
                    logger.error("DAEMON[{}] cannot execute. OptionSystemExecutePlugin is not defined.".format(self._minion.minion_identity()))
                    return

                plugin_stub = system.resolve_plugin(execute_plugin_name)

                if(plugin_stub.executable == False):
                    logger.error("DAEMON[{}] cannot execute {}. executable flag not set to True.".format(self._minion.minion_identity(), plugin_stub.id.namespace))
                    return

                logger.debug("DAEMON[{}] Loading plugins for '{}' targeting function '{}'.".format(
                        self._minion.minion_identity(),
                        execute_plugin_name,
                        execute_function_name
                    ))
                self.load(plugin_stub)

                logger.info("DAEMON[{}] Calling function '{}' from plugin '{}'.".format(self._minion.minion_identity(), execute_function_name, execute_plugin_name))
                self.call_func(plugin_stub, execute_function_name)

                logger.info("DAEMON[{}] Completed, new instance started!".format(self._minion.minion_identity()))


    @staticmethod
    def _unique(seq):
        seen = set()
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            yield x

    @staticmethod
    def _gen_load_pattern(plugin_stub):
        # base:
        depends_set = set()
        imports_set = set()
        recur_depends = dict()
        
        pattern_list = list()
        
        def add_pattern(command, stub, dependent_stubs):
            pattern_list.append(
                ("load-artifact",
                command,
                stub.output_file_location().path,
                list(map(lambda s: s.output_file_location().path, dependent_stubs))
            ))
        
        def add_depends_for(stub):
            if stub in depends_set:
                return
            add_pattern("in-mem", stub, [])
            rd = stub.gen_recursive_loaded_depends()
            recur_depends[stub] = set(rd)
            for depend in rd:
                if depend in depends_set:
                    continue
                add_pattern("in-mem", depend, [])
                drd = depend.gen_recursive_loaded_depends()
                recur_depends[depend] = set(drd)
                add_pattern("inited", depend, drd)
                depends_set.add(depend)
            add_pattern("inited", stub, rd)
            depends_set.add(stub)
        
        def add_stub(stub):
            if stub in imports_set:
                return
            add_depends_for(stub)
            imports_set.add(stub)
            for import_ in stub.loaded_imports:
                if import_ in imports_set:
                    continue
                add_stub(import_)
            rd = recur_depends[stub]
            add_pattern("final", stub, list(filter(lambda p: p not in rd, stub.gen_required_loaded_imports())))
                
        add_stub(plugin_stub)

        for stub in (depends_set - imports_set):
            add_stub(stub)
        
        return pattern_list

    def load(self, plugin_stub):
        load_pattern = ExecuterMinionSubprocess._gen_load_pattern(plugin_stub)
        for p in load_pattern:
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
                logger.error("DAEMON[{}] Encountered problem loading {}:\n\t{}".format(self.minion_identity(), plugin_stub, res))
                raise Exception("Encountered problem loading {}!".format(plugin_stub))


    def call_func(self, plugin_stub, func):
        index = plugin_stub.get_function_index(func)
        self.socket.send_pyobj(("execute", plugin_stub.output_file_location().path, index))

        self.socket.close()
        self.context.term()

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
                logger.info("DAEMON[{}] Starting execute of '{}'.".format(self._minion.minion_identity(), " ".join(command[0])))

                subproc = ExecuterMinionSubprocess(self)
                self._minion.subprocs.append(subproc)

                socket.send_pyobj((subproc.bootstrap_port,))

                time.sleep(0.01)

                subproc.execute(*command)
            except Exception as e:
                tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                logger.error("DAEMON[{}] Failed on execute of '{}':\n\t{}".format(self._minion.minion_identity(), " ".join(command[0]), tb_string))

@bootstrap_plugin("madz.daemon.minion.executer")
class ExecuterMinion(IMinion):
    current = None

    def __init__(self):
        self.banished = False
        self.spawned = False
        self.subprocs = []
        self._thread = ExecuteControlThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def minion_spawn(cls):
        if (cls.current is None):
            cls.current = ExecuterMinion()
        return cls.current._spawn()

    def _spawn(self):
        if not (self.spawned):
            self.spawned = True
            self._thread.start()
        return (self, [self.port])

    def minion_banish(self):
        self.banished = True
        for subproc in self.subprocs:
            subproc.banish()
        self._thread.join()

    @classmethod
    def minion_identity(cls):
        return "execute"

    @classmethod
    def minion_index(cls):
        return None
