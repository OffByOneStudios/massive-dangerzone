"""builder.py
@OffbyOne Studios 2013
Code to generate inter language wraper files
"""
import logging

import languages
import plugin

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

        if True or not cleaner.get_dependency():
            logger.info("Cleaning plugin: {}".format(plugin_stub))
            cleaner.clean()

