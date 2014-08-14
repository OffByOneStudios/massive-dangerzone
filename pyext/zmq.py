"""pyext/zmq.py
@OffbyOne Studios 2014
ZMQ Extensions.
"""
import time
from functools import partial as _partial

import zmq

zmq_bindfmt = "{protocol}://{hostname}:{port}".format

class ZmqBind(object):
    """Represents a point of binding, and provides features to use and serliaze it."""

    def __init__(self, protocol="tcp", host="127.0.0.1", port="*"):
        self.protocol = str(protocol)
        self.host = str(host)
        self.port = str(port)

    def __str__(self):
        return self.bind_str()

    def bind_str(self):
        """Creates the standard ZMQ bind str for this object."""
        return zmq_bindfmt(protocol=self.protocol, hostname=self.host, port=self.port)

    def random_bind_str(self):
        """Creates the random ZMQ bind str for this object."""
        old_port = self.port
        self.port = ""
        ret = self.bind_str()[:-1]
        self.port = old_port
        return ret

    def bind(self, socket):
        """Binds a zmq.Socket to this bind point."""
        if self.port == "" or self.port == "*":
            self.port = str(socket.bind_to_random_port(self.random_bind_str()))
            return
        socket.bind(self.bind_str())

    def connect(self, socket):
        """Connects a zmq.Socket to this bind point."""
        return socket.connect(self.bind_str())

    @classmethod
    def parse(self, str):
        """Attempts to, parse a string into a ZmqBind instance."""
        sections = str.split(":")
        return ZmqBind(sections[0], sections[1][2:], sections[2])

def zmq_busy(socket_try, socket_end=lambda: False, sleep_time=0.02):
    """Helper function for doing busy waits on data.

    Args:
        socket_try: The lambda to use to try and recieve from a socket (use zmq.ZMQ_NOWAIT), must retrieve non None data.
        socket_end: An optional lambda informing to stop trying to recieve the socket.
        sleep_time: Fractional time to sleep on each try (default: 0.02).
    """
    while not socket_end():
        v = zmq_try(socket_try, sleep_time=sleep_time)
        if not (v is None):
            return v

def zmq_try(socket_try, sleep_time=0.0):
    """Helper function for trying to recieve from a socket.

    Specifically catches zmq.Again.

    Args:
        socket_try: The lambda to use to try and recieve from a socket (use zmq.ZMQ_NOWAIT), must retrieve non None data.
        sleep_time: Fractional time to sleep after trying (default: 0.0).

    Returns:
        The value of `socket_try` if successful, None if fails. If the result of `socket_try` is None, returns True.

    Raises:
        [`socket_try`]: Any exceptions `socket_try` may raise.
        InterruptedError: If a sleep or zmq is interrupted.
    """
    try:
        v = socket_try()
        if v is None:
            return True
        return v
    except zmq.Again:
        try:
            time.sleep(sleep_time)
        except InterruptedError as e:
            raise e
        return None
