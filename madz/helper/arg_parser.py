"""helper/arg_parser.py
@OffbyOneStudios 2013
Helper function for interpreting command line.
"""

import argparse
import logging
import os

from ..start_modes import start_modes

logger = logging.getLogger(__name__)

def error_mode(name):
    def actual(argv, system, user_config, name=name):
        print("Error: mode {} not found.".format(name))
    return actual

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

    start_mode = start_modes.get(mode_name, error_mode(mode_name))

    start_mode(argv, system, user_config)
