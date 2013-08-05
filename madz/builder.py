"""builder.py
@OffbyOne Studios 2013
Code to generate inter language wraper files
"""
import logging

from . import plugin
from . import system_config

logger = logging.getLogger(__name__)

class BuilderSystem(object):
    """Generates inter-language wrapper files required by a plugin."""
    def __init__(self, system):
        self.system = system

    def build(self):
        for plugin in self.system.plugin_stubs:
            self.build_plugin(plugin)

    def build_plugin(self, plugin_stub):
        language = plugin_stub.language
        builder = language.make_builder()

        if self.system.config[system_config.OptionSkipDependencies] or not builder.get_dependency():
            logger.info("Building plugin: {}".format(plugin_stub))
            builder.build()

