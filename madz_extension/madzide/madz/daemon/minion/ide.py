"""madzide:madz/madzide/daemon/minion/VisualStudioGenerator.py
@OffbyOne Studios 2014
Interface for generating ide project files.
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

from madzide.idegenerator.core import *

logger = logging.getLogger(__name__)

## ECS Systems:
from madz.fileman import EcsFiles
from madz.module import EcsModules
from madz.report import EcsReports
from madz.bootstrap import EcsBootstrap
## End ECS Systems

@bootstrap_plugin("madz.daemon.minion.ide")
class IdeMinion(IMinion):
    current = None

    class IdeGeneratorThread(threading.Thread):
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

                report = []
                try:
                    with config.and_merge(Daemon.current.system.config):
                        with config.and_merge(command["user_config"]):
                            generator = get_ide_generator(command["ide"])(config)
                            generator.idegenerator_generate(command["output_directory"], command["client_path"])

                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on command '{}':\n\t{}".format(self.minion.identity(), " ".join(command[0]), tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = tb_string
                socket.send_pyobj(report)


    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = IdeMinion.IdeGeneratorThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def minion_spawn(cls):
        if (cls.current is None):
            cls.current = IdeMinion()
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
        return "ide"

    @classmethod
    def minion_index(cls):
        return None
