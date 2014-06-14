"""language.py
@OffbyoneStudios 2013
The language object pulling together all of the pieces needed for a plugin of this language.
"""

import os, sys, shutil
import logging
import subprocess

from ..c import clean as c_clean
from ...module.dependency import Dependency

logger = logging.getLogger(__name__)

class Cleaner(c_clean.Cleaner):
    """Object Which can clean Python plugins.

    Attributes:
        language: A language object
    """
    def __init__(self, language):
        """Constructor for Python Cleaner.

        Args:
            plugin_stub madz.plugin.PythonPluginStub object
        """
        self.language = language
        self.plugin_stub = language.plugin_stub


    def clean(self):
        """Cleans a plugin."""
        c_clean.Cleaner.clean(self)

    do = clean