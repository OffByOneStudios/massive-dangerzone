"""config/command.py
@OffbyOne Studios 2013
Manages the configuration of commands.
"""
from .base import *

#
# Config
#

class CommandConfig(BaseConfig):
    """This represents the configuration for a library."""
    def __init__(self, command_name, options):
        self.command_name = command_name
        BaseConfig.__init__(self, options)

    @classmethod
    def make_key(cls, command_name):
        return (cls, command_name)

    def get_key(self):
        return self.make_key(self.command_name)

    def _str_view(self):
        return "Command Config for '{}'".format(self.command_name)


class ActionConfig(BaseConfig):
    """This represents the configuration for a library."""
    def __init__(self, action_name, options):
        self.action_name = action_name
        BaseConfig.__init__(self, options)

    @classmethod
    def make_key(cls, action_name):
        return (cls, action_name)

    def get_key(self):
        return self.make_key(self.action_name)

    def _str_view(self):
        return "Action Config for '{}'".format(self.action_name)

#
# Options
#

class OptionCommandActions(BaseAppendOption): pass

class OptionExecutePlugin(BaseOption): pass
class OptionExecuteFunction(BaseOption): pass
