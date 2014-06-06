"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import sys, shutil
import logging
import subprocess

from ...core.dependency import Dependency

logger = logging.getLogger(__name__)

class Cleaner(object):
    """Object Which can clean C plugins.

    Attributes:
        plugin_stub madz.plugin.PythonPluginStub object
    """
    def __init__(self, language):
        """Constructor for C Cleaner.

        Args:
            plugin_stub madz.plugin.PythonPluginStub object
        """
        self.language = language
        self.plugin_stub = language.plugin_stub

    @classmethod
    def clean_dir(cls, dir):
        """Cleans the inputted directory.
        
        Args:
            dir: fileman.Directory object
        """
        if dir.exists():
            logger.debug("Found and cleaning directory: {}".format(dir.path))
            shutil.rmtree(dir.path)

    def clean(self):
        """Cleans a plugin."""
        self.clean_dir(self.language.wrap_directory)
        self.clean_dir(self.language.build_directory)
        self.clean_dir(self.language.output_directory)
        self.clean_dir(self.plugin_stub.directory.madz())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = ["fake"]
        return Dependency([], targets)

    do = clean
