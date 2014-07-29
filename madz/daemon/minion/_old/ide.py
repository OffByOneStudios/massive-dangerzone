
import argparse
import sys
import threading
import time
import traceback
import logging

import zmq
import pyext
import pydynecs

from madz.bootstrap import *
from ..IMinion import IMinion
from ..Daemon import Daemon

logger = logging.getLogger(__name__)

## ECS Systems:
from madz.fileman import EcsFiles
from madz.module import EcsModules
from madz.report import EcsReports
from madz.bootstrap import EcsBootstrap
## End ECS Systems

parser = argparse.ArgumentParser(description='Generate IDE project files.')
parser.add_argument('ide', type=str, help='IDE for which to generate files.')
parser.add_argument('ide', type=str, help='Directory in which to generate project files')
                
@bootstrap_plugin("madz.minion.ide")
class IdeMinion(IMinion):
    current = None
    
    EcsMinions = {
        "files": EcsFiles,
        "modules": EcsModules,
        "reports": EcsReports,
        "bootstrap": EcsBootstrap,
    }
    
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
                try:
                    command = socket.recv_pyobj(zmq.NOBLOCK)
                except zmq.ZMQError:
                    time.sleep(0.1)
                    continue
                report = []
                try:
                    generator = editors.visual_studio_generator.VisualStudioSolutionGenerator(command[0][1], Daemon.current.system, command[0][2])
                    #TODO: Do things here
                    logger.info("DAEMON[{}] Generating Solution for Project:'{}'.".format(self._minion.identity(), " ".join(command[0])))
                    generator.generate()
                    #execute_args_across(command[0], Daemon.current.system, command[1])
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on command '{}':\n\t{}".format(self._minion.identity(), " ".join(command[0]), tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = tb_string
                socket.send_pyobj(report)

                
    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = VisualStudioMinion.VisualStudioThread(self)
        self.port = Daemon.next_minion_port()

    @classmethod
    def minion_spawn(cls):
        if (cls.current is None):
            cls.current = VisualStudioMinion()
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
