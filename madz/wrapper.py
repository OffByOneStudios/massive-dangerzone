
import languages

import plugin

class WrapperSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def generate_wrappers(self):
        for plugin in self.system.plugin_stubs.values():
            self.generate_plugin_wrappers(plugin)

    def generate_plugin_wrappers(self, plugin_stub):
        wrapper_generator_class = languages.get_wrapper_generator(plugin_stub.language)
        gen = wrapper_generator_class(plugin_stub)
        gen.generate()

