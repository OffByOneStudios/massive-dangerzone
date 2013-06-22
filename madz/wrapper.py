
import languages

import plugin

class WrapperSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def wrap(self):
        for plugin in self.system.plugin_stubs:
            self.wrap_plugin(plugin)

    def wrap_plugin(self, plugin_stub):
        wrapper_generator_class = languages.get_wrapper_generator(plugin_stub.language)
        gen = wrapper_generator_class(plugin_stub)
        gen.generate()

