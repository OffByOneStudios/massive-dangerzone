"""config/current.py
@OffbyOneStudios 2013
A system for managing current config information.
"""

import contextlib

from .base import *

class CurrentConfigObject(object):
    def __init__(self, target_platform=None, source_platform=None, user_config=None, system_config=None, plugin_config=None):
        self.target_platform = target_platform
        self.source_platform = source_platform
        self.user_config = user_config
        self.system_config = system_config
        self.plugin_config = plugin_config

    def copy(self):
        return self.__class__(
            self.target_platform,
            self.source_platform,
            self.user_config,
            self.system_config,
            self.plugin_config
        )

    def compute_option(self, keys):
        merge_list = []
        for config in filter(lambda c: not (c is None), [self.user_config, self.system_config, self.plugin_config]):
            merge_list.extend(filter(lambda c: not (c is None), map(config.get_option, keys)))
        return merge(*merge_list)

    def compute(self, keys, default=None):
        option = self.compute_option(keys)
        return option.get_value() if not (option is None) else default

    def set_user_config(self, config):
        self.user_config = config

    def set_system_config(self, config):
        self.system_config = config

    @contextlib.contextmanager
    def and_system_config(self, config):
        old = self.system_config
        self.system_config = config
        yield
        self.system_config = old

    @contextlib.contextmanager
    def and_plugin_config(self, config):
        old = self.plugin_config
        self.plugin_config = config
        yield
        self.plugin_config = old


global_config = CurrentConfigObject()

