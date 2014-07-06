"""pyext/zmq.py
@OffbyOne Studios 2014
ZMQ Extensions.
"""
import time
from functools import partial as _partial

import zmq

zmq_bindfmt = "{protocol}://{hostname}:{port}".format

def zmq_busy(socket_try, socket_end=lambda: False, sleep_time=0.1):
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
