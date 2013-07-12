"""loader.py
@OffbyOneStudios 2013
Code to load plugins into memory.
"""
import logging

from . import operating_systems
from . import plugin

logger = logging.getLogger(__name__)

class LoaderSystem(object):
    """Loads plugins into the program's memory space and provides access to them."""
    def __init__(self, system):
        self.system = system
        self._operating = operating_systems.get_system()

    def load(self):
        for plugin in self.system.plugin_stubs:
            self.load_plugin(plugin)

    def load_plugin(self, plugin_stub):
        logger.info("Loading plugin: {}".format(plugin_stub))
        self._operating.load(plugin_stub)

    def get_function(self, plugin_stub, name):
        return self._operating.get_function(plugin_stub, name)

