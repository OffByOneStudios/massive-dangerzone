"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys
import logging
import subprocess

from madz.dependency import Dependency
from ..c import build as c_build

logger = logging.getLogger(__name__)

# Curently completely identical to the c implementation
# TODO(Mason): Refactor this to work off of the C implementation
class Builder(c_build.Builder):
    """Object Which can build C plugins.

    Attributes:
        plugin_stub madz.plugin.PythonPluginStub object
    """
    def __init__(self, language):
        """Constructor for C Builder.

        Args:
            plugin_stub madz.plugin.PythonPluginStub object
        """
        self.language = language
        self.compiler = language.get_compiler()
        self.plugin_stub = language.plugin_stub

