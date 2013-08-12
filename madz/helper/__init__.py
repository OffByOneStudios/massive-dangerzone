"""helper/__init__.py
@OffbyOneStudios 2013
Basic helper functions for working with plugin systems.
"""

from ..config import *

from ..action import actions

def execute_args_across(argv, system):
    parsed_command = argv[1]

    with config.and_merge(system.config):
        with config.and_merge(config.get(CommandConfig.make_key(parsed_command))):
            for action in config.get(OptionCommandActions):
                actions[action](system).do()

