"""builder.py
@OffbyOne Studios 2013
Code to generate inter language wraper files
"""
import languages

import plugin

class BuilderSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def build(self):
        for plugin in self.system.plugin_stubs:
            self.build_plugin(plugin)

    def build_plugin(self, plugin_stub):
        language = languages.get_language(plugin_stub.language).Language(plugin_stub)
        builder = language.make_builder()

        if True or not builder.get_dependency():
            builder.build()

