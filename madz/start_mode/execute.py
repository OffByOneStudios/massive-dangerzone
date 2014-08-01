"""madz/start_mode/execute.py
@OffbyOne Studios 2014
Startmode for executing a module system.
"""

import os
import sys
import queue
import threading

import zmq

from madz.bootstrap import *
import madz.start_mode.Core as core

from madz.daemon.client import Client

@bootstrap_plugin("madz.start_mode.execute")
class ExecuteStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        res = Client().invoke_minion("execute", (argv[1:], user_config))

        if isinstance(res, str):
            print(res)
            exit(1)

        (bootstrap_port,) = res
        
        bootstrapper = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "executer_bootstrap.py"))
        connecting = "tcp://127.0.0.1:{port}".format(port=bootstrap_port)
        
        print("Bootstrapping on {}.".format(connecting))

        argv = [sys.executable, bootstrapper, os.path.dirname(bootstrapper), connecting]
        if os.name == "nt":
            # Windows's execv does not behave as it should for our purposes, call script directly:
            from ..executer_bootstrap import main
            main(argv[1:])
        else:
            os.execv(argv[0], argv)
    
    @classmethod
    def startmode_identity(self):
        return "execute"