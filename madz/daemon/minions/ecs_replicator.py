
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

@bootstrap_plugin("madz.minion.ecsreplicator")
class EcsReplicatorMinion(IMinion):
    current = None

    EcsMinions = {
        "files": EcsFiles,
        "modules": EcsModules,
        "reports": EcsReports,
        "bootstrap": EcsBootstrap,
    }
    
    class ReplicatiorManagerThread(threading.Thread):
        def __init__(self, minion):
            super().__init__()
            self._minion = minion

        def run(self):
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            self._minion.command_binding.bind(socket)
            while not self._minion.banished:
                management_command = pyext.zmq_busy(lambda: socket.recv_pyobj(zmq.NOBLOCK), lambda: self._minion.banished)
                if management_command is None:
                    continue
                
                report = None
                try:
                    #TODO: set up logging report
                    logger.info("DAEMON[{}] Doing ReplicatorManagement '{}'.".format(self._minion.minion_identity(), management_command[0]))
                    report = self.invoke(self, *management_command)
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on ReplicatorManagement '{}':\n\t{}".format(self._minion.minion_identity(), management_command[0], tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = (False, tb_string)
                socket.send_pyobj(report)
        
        invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
        
        @invoke.method("start-system")
        def invoke_start_system(self, cmd, system_name):
            ret_sys = None
            if system_name in self._minion._ecs_cache:
                ret_sys = self._minion._ecs_cache[system_name]
            else:
                ret_sys = pydynecs.SyncOnDemandServer(self._minion.EcsMinions[system_name])
                self._minion._ecs_cache[system_name] = ret_sys
                ret_sys.start()
            return (ret_sys.query_bind, ret_sys.sub_bind)

    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = self.ReplicatiorManagerThread(self)
        self._ecs_cache = {}
        self.command_binding = pyext.ZmqBind()

    @classmethod
    def minion_spawn(cls):
        if (cls.current is None):
            cls.current = cls()
        return cls.current._spawn()

    def _spawn(self):
        if not (self.spawned):
            self.spawned = True
            self._thread.start()
        return (self, [self.command_binding.port])

    def minion_banish(self):
        self.banished = True
        for sys in self._ecs_cache.values():
            sys.stop()
        
        self._thread.join()

    @classmethod
    def minion_identity(cls):
        return "ecsreplicator"
    
    @classmethod
    def minion_index(cls):
        return None
