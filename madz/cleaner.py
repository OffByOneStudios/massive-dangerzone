"""builder.py
@OffbyOne Studios 2013
Code to generate inter language wraper files
"""
import logging

from . import languages
from . import plugin
from . import system_config

logger = logging.getLogger(__name__)

class CleanerSystem(object):
    """Manages the cleaning of temporary, and other, files from plugins."""
    def __init__(self, system):
        self.system = system

    def clean(self):
        for plugin in self.system.plugin_stubs:
            self.clean_plugin(plugin)

    def clean_plugin(self, plugin_stub):
        language = plugin_stub.language
        cleaner = language.make_cleaner()

        if self.system.config[system_config.OptionSkipDependencies] or not cleaner.get_dependency():
            logger.info("Cleaning plugin: {}".format(plugin_stub))
            cleaner.clean()

