"""action/clean.py
@OffbyOne Studios 2013
Action to clean temporary files in plugins.
"""
import logging

from ..config import *
from ..config import system as system_config

logger = logging.getLogger(__name__)

class CleanAction(object):
    """Manages the cleaning of temporary, and other, files from plugins."""
    def __init__(self, system):
        self.system = system

    def do(self):
        for plugin in self.system.all_plugins():
            self.clean_plugin(plugin)

    def clean_plugin(self, plugin_stub):
        language = plugin_stub.language
        cleaner = language.make_cleaner()

        if global_config.compute([system_config.OptionSystemSkipDependencies]) or not cleaner.get_dependency():
            logger.info("Cleaning plugin: {}".format(plugin_stub))
            cleaner.clean()

