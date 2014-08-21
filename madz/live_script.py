"""start_script.py
@OffbyOneStudios 2013
An import for running Madz in live mode
"""
import os, sys, imp

# logging namespace
from .helper import logging_setup as logging
from . import start_script as madz

class LiveLibrary(object):
    """Helper class for performing various startmodes on a group of modules."""
    def __init__(self, user_config_env="", log_to_stdout=True,
                 logging_file=None, module_directories=[], system_configs=[]):
        self._user_config_env = user_config_env
        self._log_to_stdout = log_to_stdout
        self._logging_file = logging_file
        self._module_directories = module_directories
        self._system_configs = system_configs

    def make_system_configs(self, plugin_configs):
        system_config = None
        for config_path in self._system_configs:
            with open(config_path) as module_file:
                config_tmp = imp.load_module("config", module_file, config_path, ('.py', 'r', imp.PY_SOURCE))
                if system_config is None:
                    system_config = config_tmp.config
                else:
                    system_config = system_config.merge(config_tmp.config)

        return system_config

    def _configure(self):
        """Set configuration and module settings"""
        # Configure Logging
        if self._log_to_stdout:
            madz.logging.bind_to_standard_out()

        if not self._logging_file is None:
            madz.logging.bind_to_file(self._logging_file)

        system_config = self.make_system_configs(self._system_configs)

        self.system = madz.core.make_system(system_config)

        # Add Plugin Directories
        for directory in self._module_directories:
            self.system.add_directory(madz.core.make_directory(directory))

    def run(self):
        self._configure()

        madz.helper.execute_system(self.system, sys.argv)

