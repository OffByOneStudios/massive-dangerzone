"""config/system.py
@OffbyOne Studios 2013
Manages the configuration of systems.
"""
from .base import *

#
# Config
#

class SystemConfig(BaseConfig):
    """Configuration for the whole system.

    """
    pass


#
# Options
#

class OptionSystemSkipDependencies(BaseOption):
    """This option determines if the system uses dependencies or not to prune what to build."""
    default_value = False


#
# Default Options
#

from .command import *

SystemConfig.default_options = [
        OptionSystemSkipDependencies(),
        CommandConfig("main", [
            OptionCommandActions(["wrap", "build", "load", "execute"]),
        ])
    ]
