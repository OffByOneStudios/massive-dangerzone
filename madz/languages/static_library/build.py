"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys
import logging
import subprocess

from madz.dependency import Dependency
from madz.languages.c import build as cbuild
logger = logging.getLogger(__name__)

class Builder(cbuild.Builder):
    """Object Which can build Static Objects into plugins.

    Attributes:
        plugin_stub madz.plugin.PythonPluginStub object
    """
    pass