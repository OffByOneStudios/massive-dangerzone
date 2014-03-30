import sys, os

from .daemon import IHandler, Server, daemon_filename

class KillHandler(IHandler):
    handler_name = "kill"

    def __init__(self):
        current_command = None

    def handle(self, obj):
        args, kwargs = obj
        argv, user_config = args

        try:
            os.remove(daemon_filename)
            Server.current.control_socket.send_pyobj("killing")
            Server.current.context.destroy(2)
            # TODO, correct exit
            exit(0)
        except Exception as e:
            return e

Server.handlers[KillHandler.handler_name] = KillHandler()

def start(argv, system, user_config):
    # TODO: Replace
    res = KillHandler.invoke({}, argv, user_config)

    print(res)
