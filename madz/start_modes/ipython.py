
import IPython
import threading
from .daemon import IHandler, Server, IFork

from .. import daemon_tools


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
    # TODO: Replace
    res = InteractivePythonHandler.invoke({"between": lambda: IPython.start_ipython()}, argv, user_config)

    print(res)
