"""start_script.py
@OffbyOneStudios 2013
An import for startup scripts.
"""

# logging namespace
from .helper import logging_setup as logging 

# config namespace
class config(object):
    from .config import UserConfig, config

    user_config = UserConfig()

    def bind_user_config(env_var, hardcode=None):
        if not (hardcode is None):
            user_config = config.UserConfig.load_from_filename(hardcode)
        else:
            user_config = config.UserConfig.load_from_env_var(env_var)
        config.user_config = user_config

# core namespace
class core(object):
    from .core.system import PluginSystem
    from .core.plugin_directory import PluginDirectory
    def make_system(system_config):
        return core.PluginSystem(system_config)

    def make_directory(directory):
        return core.PluginDirectory(directory)

# helper namespace
class helper(object):
    from .helper import execute_args_across as _execute_args_across
    def execute_system(system, argv):
       helper._execute_args_across(argv, system, config.user_config)

