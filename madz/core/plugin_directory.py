"""core/plugin_directory.py
@OffbyOne Studios 2013
Provides plugin directory objects for loading plugins.
"""
import os
import sys
import traceback
import logging

from ..config import *

from .plugin_id import *
from .plugin_stub import PluginStub

from .plugin_description.python import PluginStubFile as PythonPluginStubFile # Temporary until plugin_description chooser is finished.

logger = logging.getLogger(__name__)

class PluginDirectory(object):
    """Represents a directory potentially containing numerous plugins, which are assummed to follow canonical naming standards.

    Load the description for each plugin and validates it against it's location in the directory.
    """
    def __init__(self, directory):
        """Constructor for PluginDirectory.

        Args:
            directory: Pathname of the directory.
            partial_root: String prepended to plugin id strings before parsing. Used to place plugins in a specific subnamespace area.
        """
        self.directory = os.path.abspath(directory)

        self._plugin_stubs = {}

    def _add_plugin_stub(self, system, plugin_stub):
        self._plugin_stubs[plugin_stub.id] = plugin_stub
        system.add_plugin_stub(self, plugin_stub)

    def index_plugins(self, system, partial_root):
        """Indexs all the plugins in this directory. Adding them to the system.

        Args:
            system: The system to add the plugin to.
            partial_root: String prepended to plugin id strings before construction of PluginStubs. Used to place plugins in a specific subnamespace area.
        """
        for root, dirs, files in os.walk(self.directory):
            relroot = os.path.relpath(root, self.directory)
            splitrelroot = relroot.split(os.sep)

            for d in splitrelroot:
                if d.startswith('.'):
                    continue

            if PythonPluginStubFile.can_load_directory(root):
                file_pid = None
                try:
                    # Generate PluginID for directory
                    file_pid = PluginId.parse(".".join([partial_root] + splitrelroot))

                    logger.debug("Indexing plugin with file_pid '{}'".format(file_pid))

                    # Generate description object
                    plugin_description = PythonPluginStubFile(root)

                    # Make the stub
                    stub = PluginStub(system, plugin_description, file_pid)

                    # Check platform to make sure the plugin is valid for the target:
                    if stub.check_platform(config_target):
                        # Add stub to directory (and system)
                        self._add_plugin_stub(system, stub)
                    else:
                        logger.debug("Plugin failed platform check '{}'".format(stub.id))
                except:
                    # TODO(Mason): More specific exceptions
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("Plugin failed to load, ID per directory is '{}':\n\t{}".format(file_pid, tb_string))


