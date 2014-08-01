"""madz/start_mode/core/__init__.py
@OffbyOne Studios 2014
Core startmode features.
"""

from .IIdeGenerator import *
from .bootstrap import *

def get_ide_generator(name):
    if name in IdeGenerator_identity.current:
        return IdeGenerator_identity.current[name][IdeGenerator]
    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madzide.idegenerator.{}".format(name))
        try:
            return IdeGenerator_identity.current[name][IdeGenerator]
        except:
            pass
        return plugin[madz.bootstrap.Object]
