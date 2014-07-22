"""pyext/zmq.py
@OffbyOne Studios 2014
ZMQ Extensions.
"""
import time
from functools import partial as _partial

import zmq

zmq_bindfmt = "{protocol}://{hostname}:{port}".format

class ZmqBind(object):
    def __init__(self, protocol="tcp", host="127.0.0.1", port="*"):
        self.protocol = str(protocol)
        self.host = str(host)
        self.port = str(port)
    
    def __str__(self):
        return self.bind_str()
    
    def bind_str(self):
        return zmq_bindfmt(protocol=self.protocol, hostname=self.host, port=self.port)
    
    def random_bind_str(self):
        old_port = self.port
        self.port = ""
        ret = self.bind_str()[:-1]
        self.port = old_port
        return ret
    
    def bind(self, socket):
        if self.port == "" or self.port == "*":
            self.port = str(socket.bind_to_random_port(self.random_bind_str()))
            return
        socket.bind(self.bind_str())

    def connect(self, socket):
        return socket.connect(self.bind_str)
    
    @classmethod
    def parse(self, str):
        sections = str.split(":")
        return ZmqBind(sections[0], sections[1][2:], sections[2])
    
def zmq_busy(socket_try, socket_end=lambda: False, sleep_time=0.02):
    while not socket_end():
        v = zmq_try(socket_try, sleep_time=sleep_time)
        if not (v is None):
            return v

def zmq_try(socket_try, sleep_time=0.0):
    try:
        v = socket_try()
        if v is None:
            return True
        return v
    except zmq.Again:
        try:
            time.sleep(sleep_time)
        except InterruptedError:
            pass
        return None
