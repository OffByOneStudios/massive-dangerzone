
import languages

import plugin

class BuilderSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def build_plugins(self):
        for plugin in self.system.plugin_stubs.values():
            self.build_plugin(plugin)

    def build_plugin(self, plugin_stub):
        builder_class = languages.get_builder(plugin_stub.language)
        builder = builder_class(plugin_stub)
        builder.build()

