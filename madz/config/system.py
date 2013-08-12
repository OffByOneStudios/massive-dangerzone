"""config/system.py
@OffbyOne Studios 2013
Manages the configuration of systems.
"""
from .base import *

#
# Config
#

class SystemConfig(BaseConfig):
    """An unlabeled config applied by the system.

    This represents the information provided by the start script for the project.
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

from . import command

SystemConfig.default_options = [
        OptionSystemSkipDependencies(),
        command.CommandConfig("main", [
            command.OptionCommandActions(["wrap", "build", "load", "execute"]),
        ])
    ]
