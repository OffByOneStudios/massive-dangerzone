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

class OptionSystemExecutePlugin(BaseOption):
    """This option determines which plugin to execute."""

class OptionSystemExecuteFunctionName(BaseOption):
    """This option determines the name of the function to execute."""
    default_value = "main"

#
# Default Options
#

from . import command
