"""helper/__init__.py
@OffbyOneStudios 2013
Basic helper functions for working with plugin systems.
"""

from ..config.current import global_config
from ..config.command import *

from ..action import actions

def execute_args_across(argv, system):
    with global_config.and_system_config(system.config):
        command_config = global_config.compute([CommandConfig.make_key(argv[1])])
        for action in command_config.get(OptionCommandActions):
            actions[action](system).do()

