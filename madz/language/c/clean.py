"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys, shutil
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
            dir: Path to directory to be cleaned.
        """
        if os.path.exists(dir):
            logger.debug("Found and cleaning directory: {}".format(dir))
            shutil.rmtree(dir)

    def clean(self):
        """Cleans a plugin."""
        self.clean_dir(os.path.join(self.plugin_stub.directory, ".madz"))
        self.clean_dir(self.language.get_wrap_directory())
        self.clean_dir(self.language.get_build_directory())
        self.clean_dir(self.language.get_output_directory())
        

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = ["fake"]
        return Dependency([], targets)

    do = clean
