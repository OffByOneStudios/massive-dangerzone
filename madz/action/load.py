"""action/load.py
@OffbyOneStudios 2013
Action to load plugins.
"""
import logging
import traceback
import sys

from .. import operating_system

logger = logging.getLogger(__name__)

class LoadAction(object):
    """Loads plugins into the program's memory space and provides access to them."""
    def __init__(self, system):
        self.system = system
        self._operating = operating_system.get_system()

    def do(self):
        for plugin in self.system.all_plugins():
            self.load_plugin(plugin)

    def load_plugin(self, plugin_stub):
        logger.info("Loading plugin: {}".format(plugin_stub))
        try:
            self._operating.load(plugin_stub)
        except Exception as e:
            tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
            logger.error("Failed to load plugin '.madz' for '{}':\n\t{}".format(plugin_stub, tb_string))

    def get_function(self, plugin_stub, name):
        return self._operating.get_function(plugin_stub, name)

