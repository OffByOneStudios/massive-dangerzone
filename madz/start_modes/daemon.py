"""madz/start_modes/daemon.py
@OffbyOne Studios 2014
Daemon start mode.
"""

import os

def start(argv, system, user_config):
    # Import daemon at run time, to avoid unneccessary imports.
    from ..daemon.Daemon import Daemon, daemon_filename
    try:
        Daemon.current = Daemon(system)
        Daemon.current.start()
    finally:
        if os.path.exists(daemon_filename):
            os.remove(daemon_filename)
