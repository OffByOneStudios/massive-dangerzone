"""madz/start_modes/daemon.py
@OffbyOne Studios 2014
Daemon start mode.
"""
import os

from madz.bootstrap import *
import madz.start_mode.core as core

@bootstrap_plugin("madz.start_mode.daemon")
class DaemonStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        # Import daemon at run time, to avoid unneccessary imports.
        from madz.daemon.core.Daemon import Daemon, daemon_filename
        try:
            Daemon.current = Daemon(system)
            Daemon.current.start()
        finally:
            if os.path.exists(daemon_filename):
                os.remove(daemon_filename)
    
    @classmethod
    def startmode_identity(self):
        return "daemon"

