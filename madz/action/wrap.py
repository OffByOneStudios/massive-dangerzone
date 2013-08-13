"""action/wrap.py
@OffbyOne Studios 2013
Action for building wrapper files.
"""
import sys
import logging
import traceback

from ..config import *
from ..config import system as system_config

logger = logging.getLogger(__name__)

class WrapAction(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def do(self):
        """Wraps plugins."""
        for plugin in self.system.all_plugins():
            self.wrap_plugin(plugin)

    def wrap_plugin(self, plugin_stub):
        """Wraps a single plugin."""
        language = plugin_stub.language
        wrapper = language.make_wraper()

        if config.get(OptionSystemSkipDependencies) or (not wrapper.get_dependency()):
            logger.info("Wrapping plugin: {}".format(plugin_stub))
            try:
                wrapper.generate()
            except Exception as e:
                tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                logger.error("Failed to load plugin '.madz' for '{}':\n\t{}".format(plugin_stub, tb_string))

