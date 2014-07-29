"""madz/daemon/minion/core/__init__.py
@OffbyOne Studios 2014
Core minion features.
"""

import abc

from .IMinion import *
from .bootstrap import *

def get_minion(name):
    if name in Minion_identity.current:
        return Minion_identity.current[name][Minion]
    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madz.daemon.minion.{}".format(name))
        try:
            return Minion_identity.current[name][Minion]
        except:
            pass
        return plugin[madz.bootstrap.Object]
