"""config/user.py
@OffbyOne Studios 2013
Manages the configuration of systems from the users perspective.
"""
import os
import logging

from .base import *

logger = logging.getLogger(__name__)

#
# Config
#

class UserConfigNotFoundError(ConfigError): pass

class UserConfig(BaseConfig):
    """An unlabled config applied by the user.

    This represents the information provided by the user prior to use of the a madz project.
    """

    @classmethod
    def load_from_filename(cls, filename):
        import sys
        import traceback
        import imp
        if (not (filename is None)) and os.path.exists(filename):
            with open(filename) as module_file: #TODO(Mason): Figure out this name
                try:
                    module = imp.load_module("a_config", module_file, filename, ('.py', 'r', imp.PY_SOURCE))
                    config = getattr(module, "config")
                    if isinstance(config, UserConfig):
                        return config
                    else:
                        raise UserConfigNotFoundError("Did not find a UserConfig in the 'config' var of '{}'.")
                except:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("Failed to load user config from file '{}':\n\t{}".format(filename, tb_string))
        logger.info("Skipping user config. File not found '{}'.".format(filename))
                    
        return cls.make_default()

    @classmethod
    def load_from_env_var(cls, env_var):
        return cls.load_from_filename(os.environ.get(env_var))


#
# Options
#

