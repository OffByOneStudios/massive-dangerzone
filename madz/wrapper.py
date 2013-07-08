"""wrapper.py
@OffbyOne Studios 2013
Code to generate inter-language wrapper files.
"""
import logging

import languages
import plugin

logger = logging.getLogger(__name__)

class WrapperSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def wrap(self):
        """Wraps all plugins."""
        for plugin in self.system.plugin_stubs:
            self.wrap_plugin(plugin)

    def wrap_plugin(self, plugin_stub):
        """Wraps a single plugin."""
        language = plugin_stub.language
        wrapper = language.make_wraper()

        # TODO(Mason): remove this hack.
        if True or not gen.get_dependency():
            logger.info("Wrapping plugin: {}".format(plugin_stub))
            wrapper.generate()

