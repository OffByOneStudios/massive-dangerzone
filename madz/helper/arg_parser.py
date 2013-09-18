"""helper/arg_parser.py
@OffbyOneStudios 2013
Helper function for interpreting command line.
"""

import argparse
import logging

from ..config import *
from ..action import actions

from . import logging_setup

logger = logging.getLogger(__name__)

def generate_parser(valid_commands):
    """Creates a parser for actions on a plugin system.
    
    Args:
        valid_commands: A list of commands which are allowed to be performed on a plugin system.
        
    Returns:
        An argparse.ArgumentParser object
    """
    parser = argparse.ArgumentParser(description='Perform actions across a plugin system.')

    parser.add_argument("commands",
        action='store',
        nargs='+',
        choices=valid_commands,
        help="The command(s) to execute on the system, in order.")
    parser.add_argument("-m", "--modes",
        action='append',
        default=[],
        nargs='*',
        help="The modes to apply to the system before executing it.")
    parser.add_argument("-l", "--log-level",
        action='store',
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="The log level to use for this execution.")
    parser.add_argument("-p", "--plugins",
        action='append',
        default=None,
        nargs='*',
        help="The plugins to perform the action on, not recommended for some actions.")

    return parser

def execute_args_across(argv, system, user_config):
    """Executes the commands from a list of plugin configurations across a provided system from the command line.
    
    Args:
        argv: List of arguments from the command line
        system: A system object which the Configurations will be applied to
        user_config: A list of Configurations
    """
    # Apply system and user config.
    with config.and_merge(system.config):
        with config.and_merge(user_config):
            # Build valid command list for arg parsing
            # We can't build modes because that would require us to apply the command config.
            valid_commands = list(map(lambda c: c.label, config.get_option_type(CommandConfig)))

            # Parse the arguments
            args = generate_parser(valid_commands).parse_args(argv[1:])

            # Setup logging level
            if not (logging_setup._log_ch is None):
                logging_setup._log_ch.setLevel(logging_setup._log_level_name_index[args.log_level])

            # Setup active plugins
            if not (args.plugins is None):
                active_plugins = [item for sublist in args.plugins for item in sublist]
                system.set_active_plugins(system.resolve_plugins(active_plugins))

            # Expand out the parsed arguments
            parsed_commands = args.commands
            parsed_modes = args.modes

            # Apply Commands
            for parsed_command in parsed_commands:
                logger.debug("Starting command '{}'".format(parsed_command))
                with config.and_merge(config.get(CommandConfig.make_key(parsed_command))):
                    # Apply Modes
                    old_config_state = config.copy_state()
                    for parsed_mode in [item for sublist in parsed_modes for item in sublist]:
                        logger.debug("Entering mode '{}'".format(parsed_mode))
                        # TODO: Check for non-existent ModeConfigs
                        config.add(config.get(ModeConfig.make_key(parsed_mode)))

                    # Do Actions
                    for action in config.get(OptionCommandActions):
                        logger.debug("Starting action '{}'".format(action))
                        actions[action](system).do()

                    # Remove Modes, safely clean up config.
                    config.set_state(old_config_state)
