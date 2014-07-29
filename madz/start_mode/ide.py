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
import madz.start_mode.core as core

from ..daemon import Client

@bootstrap_plugin("madz.start_mode.ide")
class ExecuteStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        res = Client().invoke_minion("ide", (argv[1:], user_config))

        print(res)
    
    @classmethod
    def startmode_identity(self):
        return "ide"