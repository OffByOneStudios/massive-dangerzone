"""madz/start_mode/execute.py
@OffbyOne Studios 2014
Startmode for executing a module system.
"""

import os
import sys
import queue
import threading

import zmq

from ..daemon import Client

stdin = sys.stdin.buffer
stdout = sys.stdout.buffer
stderr = sys.stderr.buffer

commqueue = queue.Queue()
stop_event = threading.Event()

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
        if stop_event.isSet() or len(line) == 0:
            break

def start(argv, system, user_config):
    res = Client().invoke_minion("execute", (argv[1:], user_config))

    if isinstance(res, str):
        print(res)
        exit(1)

    (bootstrap_port,) = res
    
    bootstrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "executer_bootstrap.py"))
    connecting = "tcp://127.0.0.1:{port}".format(port=bootstrap_port)
    
    print("Bootstrapping on {}.".format(connecting))

    argv = [sys.executable, bootstrapper, os.path.dirname(bootstrapper), connecting]
    if os.name == "nt":
        # Windows's execv does not behave as it should for our purposes, call script directly:
        from ..executer_bootstrap import main
        main(argv[1:])
    else:
        os.execv(argv[0], argv)
