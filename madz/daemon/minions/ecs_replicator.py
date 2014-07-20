
import sys
import threading
import time
import traceback

import zmq
import pyext
import pydynecs

from madz.bootstrap import *
from ..IMinion import IMinion
from ..Daemon import Daemon

## ECS Systems:
from ...module import EcsFiles
## End ECS Systems

@bootstrap_plugin("madz.minion.ecs_replicator")
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
                report = None
                try:
                    #TODO: set up logging report
                    logger.info("DAEMON[{}] Doing ReplicatorManagement '{}'.".format(self._minion.minion_identity(), " ".join(management_command[0])))
                    report = self.invoke(management_command)
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("DAEMON[{}] Failed on ReplicatorManagement '{}':\n\t{}".format(self._minion.minion_identity(), " ".join(management_command[0]), tb_string))
                    pass #TODO: Create exception report, combine and send
                    report = tb_string
                socket.send_pyobj(report)
        
        invoke = pyext.multimethod(pyext.ArgMatchStrategy(True))
        
        @invoke.method("start-system"):
        def invoke_start_system(self, cmd, system_name):
            ret_sys = None
            if system_name in self._minion._ecs_cache:
                ret_sys = self._minion._ecs_cache[system_name]
            else:
                ret_sys = pydynecs.SyncOnDemandServer(self._minion.EcsMinions[system_name])
                ret_sys.start()
            return (ret_sys.query_binding, ret_sys.sub_binding)

    def __init__(self):
        self.banished = False
        self.spawned = False
        self._thread = self.ReplicatiorManagerThread(self)
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
        self._thread.join()

    @classmethod
    def minion_identity(cls):
        return "ecsreplicator"
    
    @classmethod
    def minion_index(cls):
        return None
