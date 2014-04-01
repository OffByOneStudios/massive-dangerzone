
import os

from ..daemon.Daemon import Daemon, daemon_filename
from .. import daemon_tools

def start(argv, system, user_config):
    try:
        Daemon.current = Daemon(system)
        daemon_tools.CurrentSystem = system
        Daemon.current.start()
    finally:
        if os.path.exists(daemon_filename):
            os.remove(daemon_filename)
