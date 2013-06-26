"""wrapper.py
@OffbyOne Studios 2013
Code to generate inter-language wrapper files.
"""
import languages

import plugin

class WrapperSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def wrap(self):
        """# TODO(mason) What do these two functions do"""
        for plugin in self.system.plugin_stubs:
            self.wrap_plugin(plugin)

    def wrap_plugin(self, plugin_stub):
        """# TODO(mason) What do these two functions do"""
        wrapper_generator_class = languages.get_wrapper_generator(plugin_stub.language)
        gen = wrapper_generator_class(plugin_stub)

        if gen.get_dependency():
            gen.generate()