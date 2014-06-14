"""madz/start_mode/ipython.py
@OffbyOne Studios 2014
Startmode for embedding ipython within a running daemon.
"""

import IPython
import threading
from .daemon import IHandler, Server, IFork


class IPythonThread(threading.Thread):
    """Thread for the IPython repl"""
    def run(self):
        try:
            IPython.embed_kernel(module=daemon_tools, local_ns=daemon_tools.__dict__)
        except:
            print("Unable to Start IPython kernel")

class IPythonFork(IFork):
    """tmp class to keep zmq threads from hanging"""
    def run(self):
        IPython.embed_kernel(module=daemon_tools, local_ns=daemon_tools.__dict__)

class InteractivePythonHandler(IHandler):
    handler_name = "ipython"

    def __init__(self):
        current_command = None

    def handle(self, obj):
        args, kwargs = obj
        argv, user_config = args

        try:
            #t = IPythonThread()
            #t.start()
            return IPythonFork()

        except Exception as e:
            return e

Server.handlers[InteractivePythonHandler.handler_name] = InteractivePythonHandler()

def start(argv, system, user_config):
    res = client.invoke_minion("ipython", (argv, user_config))

    print(res)
