"""languages/python/build.py
@OffbyOneStudios
Code to Build Python Plugins
"""
import os, sys, shutil, logging
import subprocess

import shared

import madz.languages.c.build as c_build
from madz.dependency import Dependency

logger = logging.getLogger(__name__)

class Builder(c_build.Builder):
    """Object Which can build Python plugins.

    Attributes:
        plugin_stub madz.plugin.PythonPluginStub object
    """
    lang = shared.LanguageShared

    def __init__(self, language):
        """Constructor for Python Builder.

        Args:
            plugin_stub madz.plugin.PythonPluginStub object
        """

        self.language = language
        self.compiler = language.get_compiler()
        self.plugin_stub = language.plugin_stub

    def prep(self):
        """Performs any pre-compile stage prep work for plugin."""
        if not (os.path.exists(self.language.get_build_directory())):
            os.makedirs(self.language.get_build_directory())

        if not (os.path.exists(self.language.get_output_directory())):
            os.makedirs(self.language.get_output_directory())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [self.language.get_output_file()]
        dependencies = self.language.get_c_source_files()
        dependencies.append(self.language.get_c_code_filename())
        return Dependency(dependencies, targets)

