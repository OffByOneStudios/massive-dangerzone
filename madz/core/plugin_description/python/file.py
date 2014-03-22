"""core/plugin_description/python/file.py
@OffbyOneStudios 2013
Provides a file loader for python plugin descriptions.
"""
import os
import imp

from .._base import *

class PythonPluginStubFile(object):
    def __init__(self, directory):
        """Default Constructor
        Args:
            directory: 
        """
        self._directory = directory
        self._py_module_file = directory.file("__plugin__.py")
        self._init_module()

    @classmethod
    def can_load_directory(cls, directory):
        """Returns true if the directory contains a potential python plugin description."""
        return directory.file_exists("__plugin__.py")

    def _init_module(self):
        with self._py_module_file.open("r") as module_file:
            # TODO(Mason): Exception for failure to load
            # TODO(Mason): Exception for missing plugin
            # TODO(Mason): Figure out name variable
            self._module = imp.load_module("test", module_file, self._py_module_file._path, ('.py', 'r', imp.PY_SOURCE))
            self._plugin = getattr(self._module, "plugin")

    @property
    def directory(self):
        return self._directory

    @property
    def plugin_description(self):
        return self._plugin

    def get_plugin_loader_files(self):
        return [self._py_module_file] + self._plugin.description.dependency_files(self.directory)
