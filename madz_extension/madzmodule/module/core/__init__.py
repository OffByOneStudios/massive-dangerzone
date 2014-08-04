"""madzmodule:module/core/__init__.py
@OffbyOne Studios 2014
Module Operations
"""

import os

from .IModuleOperation import *
from .bootstrap import *


def get_moduleoperation(name):
    if name in ModuleOperation_identity.current:
        return ModuleOperation_identity.current[name][ModuleOperation]

    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madzmodule.module.{}".format(name))
        try:
            return ModuleOperation_identity.current[name][ModuleOperation]
        except:
            pass
        return plugin[madz.bootstrap.Object]
