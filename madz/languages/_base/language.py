
import abc
import os

class BaseLanguage(object):
    """Base language object."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, plugin_stub, language_config):
        self.plugin_stub = plugin_stub
        self.config = language_config

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

    def get_plugin_filename(self):
        return self.plugin_stub._py_module_filename

    def get_output_directory(self):
        return os.path.join(self.plugin_stub.abs_directory, ".output")

    def get_output_file(self):
        return os.path.join(self.get_output_directory(), self.plugin_stub.id.namespace + ".madz")

