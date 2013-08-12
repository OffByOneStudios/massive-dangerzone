"""config/command.py
@OffbyOne Studios 2013
Manages the configuration of commands.
"""
from .base import *

#
# Config
#

class CommandConfig(BaseLabeledConfig):
    """This represents the configuration for a library."""
    pass

#
# Options
#

class OptionCommandActions(BaseAppendOption): pass

class OptionExecutePlugin(BaseOption): pass
class OptionExecuteFunction(BaseOption): pass
