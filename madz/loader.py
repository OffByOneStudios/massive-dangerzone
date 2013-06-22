
import operating_systems

import plugin

class LoaderSystem(object):
    """Loads plugins into the program's memory space and provides access to them."""
    def __init__(self, system):
        self.system = system
        self._operating = operating_systems.get_system()

    def load(self):
        for plugin in self.system.plugin_stubs:
            self.load_plugin(plugin)

    def load_plugin(self, plugin_stub):
        self._operating.load(plugin_stub)

