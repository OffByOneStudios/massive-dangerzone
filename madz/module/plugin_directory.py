"""core/plugin_directory.py
@OffbyOne Studios 2013
Provides plugin directory objects for loading plugins.
"""
import os
import sys
import traceback
import logging

from ..config import *
from .. import fileman

from .plugin_id import *
from .plugin_stub import PluginStub

from .plugin_description.python import PluginStubFile as PythonPluginStubFile # Temporary until plugin_description chooser is finished.

logger = logging.getLogger(__name__)

class PluginDirectory(object):
    """Represents a directory potentially containing numerous plugins, which are assummed to follow canonical naming standards.

    Loads the description for each plugin and validates it against it's location in the directory.
    """
    def __init__(self, directory):
        """Constructor for PluginDirectory.

        Args:
            directory: Pathname of the directory.
        """
        self.directory = fileman.new(directory)
        self._plugin_stubs = {}

    def _add_plugin_stub(self, system, plugin_stub):
        """Adds a plugin stub to a system
        
        Args:
            system: The system to add the plugin stub to.
            plugin_stub; The plugin stub to be added to the provided system.
        """
        self._plugin_stubs[plugin_stub.id] = plugin_stub
        system.add_plugin_stub(self, plugin_stub)

    def index_plugins(self, system, partial_root):
        """Indexes all the plugins in this directory, adding them to the system.

        Args:
            system: The system to add the indexed plugins to.
            partial_root: String prepended to plugin id strings before construction of PluginStubs. Used to place plugins in a specific subnamespace area.
        """
        for root, dirs, files in os.walk(self.directory.path):
            relroot = os.path.relpath(root, self.directory.path)
            splitrelroot = relroot.split(os.sep)

            # Skips hidden directories
            hiddendir = False
            for d in splitrelroot:
                if d.startswith('.'):
                    hiddendir = True
            if hiddendir:
                continue

            if PythonPluginStubFile.can_load_directory(fileman.new(root)):
                file_pid = None
                try:
                    # Generate PluginID for directory
                    file_pid = PluginId.parse(".".join([partial_root] + splitrelroot))

                    logger.debug("Indexing plugin with file_pid '{}'".format(file_pid))

                    # Generate description object
                    plugin_description = PythonPluginStubFile(fileman.new(root))

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

    def __str__(self):
        return str(self.directory.path)

"""
#Example Usage of PluginDirectory

directory = PluginDirectory("/Plugins")

directory.index_plugins(physics, "/ragdoll")
"""
