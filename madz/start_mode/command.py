"""madz/start_mode/command.py
@OffbyOne Studios 2014
Srtartmode for executing a build command across the plugin system.
"""

from madz.bootstrap import *
import madz.start_mode.core as core

from ..daemon import Client

@bootstrap_plugin("madz.start_mode.command")
class CommandStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        res = Client().invoke_minion("command", (argv, user_config))

        print(res)
    
    @classmethod
    def startmode_identity(self):
        return "command"