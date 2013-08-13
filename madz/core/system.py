"""system.py
@OffbyOneStudios 2013
Code to create Plugin Systems
"""
import os
import sys
import copy
import logging
import traceback

from ..config import system
from .plugin_stub import *
from .plugin_resolver import PluginResolver

logger = logging.getLogger(__name__)

class PluginSystem(object):
    """ A plugin system object which manages a universe of objects.

    Responsible for managing global information.

    """
    def __init__(self, config):
        """Constructor for PluginSystem.

        Args:
            config: A SystemConfig object describing the configuration of the universe represented by this object.
        """
        self.config = config

        self.directories = []
        self._plugin_stubs = []

        # TODO: Use config system to generate:
        self.plugin_resolver = PluginResolver()

    def add_directory(self, directory, partial_root=""):
        """Adds a PluginDirectory to the list of directories to retrieve plugins from.

        Args:

        """
        self.directories.append((directory, partial_root))

    def add_plugin_stub(self, directory, plugin_stub):
        """Add plugin_stub to the system, only PluginDirectories, or virtual plugin providers, should call this.

        Args:
            directory: The directory object responsible for reporting the plugin.
            plugin_stub: the PluginStub object to add
        """
        self._plugin_stubs.append((plugin_stub, directory))
        self.plugin_resolver.add_plugin_stub(plugin_stub)

    def resolve(self, string):
        """Retrieve plugin by namespace.

        Args:
            string: A string parse-able by a PartialPluginId.

        Returns:
            The PluginStub that is best associated with the given PartialPluginId.
        """
        return self.plugin_resolver.get_plugin(string)

    def all_plugins(self):
        return map(lambda p: p[0], self._plugin_stubs)

    def _init_plugin(self, plugin):
        resolve_func = lambda id: self.plugin_resolver.get_plugin(id.namespace)

        if not(plugin.inited):
            for dep_id in plugin.depends:
                self._init_plugin(resolve_func(dep_id))

            if not plugin.init_requires(resolve_func):
                logger.error("Plugin {} failed to load.".format(plugin.id))
            plugin.inited = True

    def index(self):
        """Searches all PluginDirectory objects for plugins and indexs them into the universe."""
        for directory, partial_root in self.directories:
            logger.debug("Indexing plugins from '{}' into '{}'".format(directory, partial_root))
            directory.index_plugins(self, partial_root)

        for plugin_stub, directory in self._plugin_stubs:
            logger.debug("Initializing plugin '{}'".format(plugin_stub))
            try:
                self._init_plugin(plugin_stub)
            except:
                tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                logger.error("Plugin failed to init: '{}':\n\t{}".format(plugin_stub, tb_string))



