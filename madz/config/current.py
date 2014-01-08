"""config/current.py
@OffbyOneStudios 2013
A system for managing current config information.
"""

import contextlib

from .base import *
from .platform import *

class ConfigWorld(object):
    """Defines a world of configurations from a list of configs.
    
    Attributes:
        config_list: A list of Configuration objects.
    """
    def __init__(self, config_list=[]):
        self.config_list = config_list

    def copy_state(self):
        """Returns a copy of the current configuration list"""
        return list(self.config_list)

    def set_state(self, state_list):
        """Sets the current config_list to the inputted list of configurations.
        
        Args:
            state_list: A list of configurations.
        """
        self.config_list = state_list

    def save(self):
        """Merges configs and saves.
        
        Returns:
            MergedConfig object
        """
        return self.get_merged_config()

    def get_merged_config(self):
        """Returns a MergedConfig object. Called in save."""
        return merge(MergedConfig(), *self.config_list)

    def get_option(self, key):
        """Returns an option from the provided key.
        
        Args:
            key: A named key string
            
        Returns:
            An Option object
        """
        return self.get_merged_config().get_option(key)

    def get_option_type(self, key):
        """Returns the option type of the Option object found from the provided key.
        
        Args:
            key: A named key string
            
        Returns:
            The class of the Option object found from the inputted key.
        """
        return \
            map(lambda t: t[1],
                filter(lambda k: k[0] == key,
                    map(lambda c: (c.__class__, c), 
                        self.get_merged_config().get_options())))
            

    def get(self, key, default=None):
        #TODO(Mason): Make default do something
        """Returns the option found from the provided key.
        
        Args:
            key: A named key string

        Returns:
            An Option object
        """
        option = self.get_option(key)
        return option.get_value() if not (option is None) else default

    def add(self, config):
        """Appends a Configuration object to the end of the current config_list.
        
        Args:
            config: A Configuration objedt to be added to the end of the current config_list.
        """
        self.config_list.append(config)

    def pop(self):
        """Removes and returns the Configuration object from the front of the current config_list.
        
        Returns:
            The Configuration object at the front of the config_list.
        """
        return self.config_list.pop()

    def remove(self, config_key):
        """Removes a configuration which matches the configuration key from the current config_list.
        
        Args:
            config_key: A named key string
        """
        self.config_list = list(filter(lambda c: c.get_key() != config_key, self.config_list))

    @contextlib.contextmanager
    def and_merge(self, config):
        old_state = self.copy_state()
        self.add(config)
        try:
            yield
        finally:
            self.set_state(old_state)


config = ConfigWorld()
config_target = ConfigWorld([PlatformConfig.make_default()])
config_source = ConfigWorld([PlatformConfig.make_default()])