"""madzide:madz.daemon.minion.module.py
@OffbyOne Studios 2014
Minion for performing operations on modules
"""

import sys
import threading
import time
import traceback
import logging

import zmq
import pyext
import pydynecs

from madz.bootstrap import *
from madz.config import *
from madz.daemon.minion.core import IMinion
from madz.daemon.core import Daemon

from madzmodule.module.core import *
from madzmodule.language.core import *

@bootstrap_plugin("madz.daemon.minion.module")
class ModuleMinion(IMinion):
    current = None

    class ModuleThread(threading.Thread):
        def __init__(self, minion):
            super().__init__()
            Daemon.current.system.index()
            self._minion = minion

        def run(self):
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://127.0.0.1:{port}".format(port=self._minion.port))
            while not self._minion.banished:
                command = pyext.zmq_busy(lambda: socket.recv_pyobj(zmq.NOBLOCK),
                    socket_end=lambda s=self: s._minion.banished)

                if command is None:
                    continue

                report = None
                try:
                    operation = get_moduleoperation(command["start_mode"])()
                    operation.moduleoperation_perform(**dict(filter(lambda k: k[0] != "start_mode", command.items())))



                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on command '{}':\n\t{}".format(self.minion.identity(), " ".join(command[0]), tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = tb_string
                socket.send_pyobj(report)


    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = ModuleMinion.ModuleThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def minion_spawn(cls):
        if cls.current is None:
            cls.current = ModuleMinion()
        return cls.current._spawn()

    def _spawn(self):
        if not (self.spawned):
            self.spawned = True
            self._thread.start()
        return (self, [self.port])

    def minion_banish(self):
        self.banished = True
        self._thread.join()

    @classmethod
    def minion_identity(cls):
        return "module"

    @classmethod
    def minion_index(cls):
        return None
