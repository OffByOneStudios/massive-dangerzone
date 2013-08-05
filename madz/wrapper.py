"""wrapper.py
@OffbyOne Studios 2013
Code to generate inter-language wrapper files.
"""
import logging

from . import languages
from . import plugin
from . import system_config

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

        if self.system.config[system_config.OptionSkipDependencies] or not wrapper.get_dependency():
            logger.info("Wrapping plugin: {}".format(plugin_stub))
            wrapper.generate()

