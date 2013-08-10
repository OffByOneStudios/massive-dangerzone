"""core/plugin_description/python/file.py
@OffbyOneStudios 2013
Provides a file loader for python plugin descriptions.
"""
import os
import imp

from .._base import *

class PythonPluginStubFile(object):
    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        self._py_module_filename = os.path.join(self.directory, "__plugin__.py")
        self._init_module()

    @classmethod
    def can_load_directory(cls, directory):
        """Returns true if the directory contains a potential python plugin description."""
        return os.path.exists(os.path.join(directory, "__plugin__.py"))

    def _init_module(self):
        with open(self._py_module_filename) as module_file:
            # TODO(Mason): Exception for failure to load
            # TODO(Mason): Exception for missing plugin
            # TODO(Mason): Figure out name variable
            self._module = imp.load_module("test", module_file, self._py_module_filename, ('.py', 'r', imp.PY_SOURCE))
            self._plugin = getattr(self._module, "plugin")

    def get_directory(self):
        return self.directory

    def get_plugin_description(self):
        return self._plugin
