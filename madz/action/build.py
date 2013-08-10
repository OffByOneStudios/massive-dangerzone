"""action/build.py
@OffbyOne Studios 2013
Action for building plugin source code into binaries.
"""
import logging

from ..config import *
from ..config import system as system_config

logger = logging.getLogger(__name__)

class BuildAction(object):
    """Builds plugin source code into binaries."""
    def __init__(self, system):
        self.system = system

    def do(self):
        for plugin in self.system.all_plugins():
            self.build_plugin(plugin)

    def build_plugin(self, plugin_stub):
        language = plugin_stub.language
        builder = language.make_builder()

        if global_config.compute([system_config.OptionSystemSkipDependencies]) or not builder.get_dependency():
            logger.info("Building plugin: {}".format(plugin_stub))
            builder.build()

