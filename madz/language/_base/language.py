
import abc
import os

from ...config import *
from ...config.language import *

class BaseLanguage(object):
    """Base language object."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_language_name(self):
        pass

    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub

    @abc.abstractmethod
    def make_cleaner(self):
        pass

    @abc.abstractmethod
    def make_loader(self):
        pass

    @abc.abstractmethod
    def make_builder(self):
        pass

    @abc.abstractmethod
    def make_wrapper(self):
        pass

    def supported_extensions(self):
        return []

    def get_plugin_description_files(self):
        return self.plugin_stub._plugin_loader_files

    def get_output_directory(self):
        return os.path.join(self.plugin_stub.directory, ".output")

    def get_output_file(self):
        return os.path.join(self.get_output_directory(), self.plugin_stub.id.namespace + ".madz")

