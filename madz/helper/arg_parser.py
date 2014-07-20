"""helper/arg_parser.py
@OffbyOneStudios 2013
Helper function for interpreting command line.
"""

import argparse
import logging
import os
from madz.bootstrap import *

from madz.start_mode.core import *

logger = logging.getLogger(__name__)

def error_mode(name):
    class Actual:
        _name=name
        def startmode_start(self, argv, system, user_config):
            print("Error: mode '{}' not found:\n\tArgs: {}\n\tSystem: {}\n====Config====\n{}".format(self._name, argv, system, user_config))
    return Actual

def execute_args_across(argv, system, user_config):
    """Executes the commands from a list of plugin configurations across a provided system from the command line.
    
    Args:
        argv: List of arguments from the command line
        system: A system object which the Configurations will be applied to
        user_config: A list of Configurations
    """
    # Apply system and user config.
    mode_name = argv[1]
    argv = [argv[0]] + argv[2:]

    #try:
    start_mode = get_start_mode(mode_name)
    #except:
    #    start_mode = None
        
    if start_mode is None:
        start_mode = error_mode(mode_name)

    start_mode = start_mode()
        
    start_mode.startmode_start(argv, system, user_config)
