
import os
import abc
import logging

logger = logging.getLogger(__name__)

daemon_filename = "madz.daemon"

class IHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, obj):
        pass

    handler_name = None
    @classmethod
    def invoke(cls, our_args, *args, **kwargs):
        context = zmq.Context()

        if (os.path.exists(daemon_filename)):
            with open(daemon_filename, "r") as f:
                daemon_port = int(f.read(8))
        else:
            raise Exception("Daemon port file:{} does not exists".format(os.path.abspath(daemon_filename)))

        control_socket = context.socket(zmq.REQ)
        control_socket.connect("tcp://127.0.0.1:{port}".format(port=daemon_port))

        control_socket.send_pyobj((cls.handler_name, (args, kwargs)))
        our_args.get("between", lambda: None)()
        res = control_socket.recv_pyobj()

        control_socket.close(-1)
        context.term()

        return res

import zmq

class Server(object):
    current = None

    handlers = {}

    def __init__(self, system):
        self.context = zmq.Context()
        Server.system = system

    def start(self, **kwargs):
        try:
            port = int(kwargs.get("port", 16239))
            force = bool(kwargs.get("force", False))
        except Exception as e:
            raise Exception("Failed to parse arguments.") from e

        try:
            if (not force) and os.path.exists(daemon_filename):
                raise Exception("Daemon file already exists, may need to delete.")
            with open(daemon_filename, "w") as f:
                f.write(str(port))
        except Exception as e:
            raise Exception("Failed to write daemon file.") from e

        self.control_socket = self.context.socket(zmq.REP)
        self.control_socket.bind("tcp://127.0.0.1:{port}".format(port=port))
        logger.info("Bound to: {}.".format(port))

        while True:
            (handler, obj) = self.control_socket.recv_pyobj()
            if not (handler in self.handlers):
                logger.warning("Handler '{}': Attempted but does not exist.")
                continue

            handler = self.handlers[handler]
            logger.info("Handling {}.".format(handler.handler_name))
            res = handler.handle(obj)
            logger.info("Done {}.".format(handler.handler_name))

            self.control_socket.send_pyobj(res)


def start(argv, system, user_config):
    try:
        Server.current = Server(system)
        Server.current.start()
    finally:
        if os.path.exists(daemon_filename):
            os.remove(daemon_filename)
