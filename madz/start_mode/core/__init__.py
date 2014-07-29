"""madz/start_mode/core/__init__.py
@OffbyOne Studios 2014
Core startmode features.
"""

from .IStartMode import *
from .bootstrap import *

def get_start_mode(name):
    if name in StartMode_identity.current:
        return StartMode_identity.current[name][StartMode]
    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madz.start_mode.{}".format(name))
        try:
            return StartMode_identity.current[name][StartMode]
        except:
            pass
        return plugin[madz.bootstrap.Object]
