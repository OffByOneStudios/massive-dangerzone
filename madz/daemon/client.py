import os

import zmq
import pyext

from . import *

class Client(object):
    def __init__(self, daemon_filename=None):
        if daemon_filename is None:
            daemon_filename = daemon_filename
        self._daemon_file = daemon_filename

    def binding(self, port=None):
        daemon_port = None
        if not (port is None):
            try:
                daemon_port = int(port)
            except:
                pass
        elif (os.path.exists(daemon_filename)):
            try:
                with open(daemon_filename, "r") as f:
                    daemon_port = int(f.read(8))
            except:
                pass
        
        if daemon_port is None:
            raise Exception("Daemon port file '{}' does not exist, and port '{}' is not port.".format(
                os.path.abspath(daemon_filename),
                port))

        return "tcp://127.0.0.1:{port}".format(port=daemon_port)

    def invoke_daemon(self, command, sub_command=""):
        """Invokes a command on the daemon
        """
        context = zmq.Context()

        control_socket = context.socket(zmq.REQ)
        control_socket.connect(self.binding())

        control_socket.send_multipart(list(map(lambda c: str(c).encode("utf-8"), [command, sub_command])))
        
        res = pyext.zmq_busy(lambda: control_socket.recv_pyobj(zmq.NOBLOCK))

        control_socket.close(-1)
        context.term()

        return res

    def invoke_minion(self, minion, py_obj, between=lambda: None):
        """Invokes a command on a minion
        """

        res = self.invoke_daemon("minion", minion)

        context = zmq.Context()

        control_socket = context.socket(zmq.REQ)
        control_socket.connect(self.binding(res[0]))

        control_socket.send_pyobj(py_obj)
        between()
        res = pyext.zmq_busy(lambda: control_socket.recv_pyobj(zmq.NOBLOCK))

        control_socket.close(-1)
        context.term()

        return res

class MinionClientProxy(object):
    """Pretends to be a minion on the client side, an RPC object."""