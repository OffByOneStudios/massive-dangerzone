
import IPython

from .daemon import IHandler, Server

class InteractivePythonHandler(IHandler):
    handler_name = "ipython"

    def __init__(self):
        current_command = None

    def handle(self, obj):
        args, kwargs = obj
        argv, user_config = args

        try:
            IPython.embed_kernel()
        except Exception as e:
            return e

Server.handlers[InteractivePythonHandler.handler_name] = InteractivePythonHandler()

def start(argv, system, user_config):
    # TODO: Replace
    res = InteractivePythonHandler.invoke({"between": lambda: IPython.start_ipython()}, argv, user_config)

    print(res)
