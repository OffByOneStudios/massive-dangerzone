"""madzmodule:start_mode/core/init.py
@OffbyOne Studios 2014
Module Startmodes
"""

import os

from .IStartMode import *
from .bootstrap import *

import madzmodule.start_mode

def get_startmode(name):
    if name in StartMode_identity.current:
        return StartMode_identity.current[name][StartMode]
    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madzmodule.start_mode.{}".format(name))
        try:
            return StartMode_identity.current[name][StartMode]
        except:
            pass
        return plugin[madz.bootstrap.Object]

def all_startmodes():
    for name in madzmodule.start_mode.__path__:
        for mod in os.listdir(name):
            if mod != "core":
                if mod.endswith(".py"):
                    mod = mod[:-3]
                yield get_startmode(mod)
