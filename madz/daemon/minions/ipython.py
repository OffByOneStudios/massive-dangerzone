import threading
import time

import zmq
import ipython

from madz.bootstrap import *
from ..IMinion import IMinion
from ..Daemon import Daemon

@bootstrap_plugin("madz.minion.InteractivePython")
class InteractivePythonMinion(IMinion):
    current = None

    class PythonThread(threading.Thread):
        def __init__(self, minion):
            self._minion = minion

        def run(self):
            ipython.embed_kernel()
            print("AFTER EMBED!!!!")

    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = CommandThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def spawn(cls):
        if (cls.current == None):
            cls.current = CommandMinion()
        cls.current._spawn()

    def _spawn(self):
        if (self.spawned == True):
            return
        self.spawned = True
        self._thread.start()

    def banish(self):
        banished = True
        self._thread.join()

    @classmethod
    def identity(cls):
        return "ipython"