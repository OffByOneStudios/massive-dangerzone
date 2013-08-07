import abc

class BaseCompiler(object):
    """The base compiler object."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, language, compiler_config):
        self.language = language
        self.config = compiler_config

    class BuildType():
        DynamicPlugin = 0
        StaticPlugin = 1

    @abc.abstractmethod
    def build(self, type):
        """Builds a plugin of the given type."""
        pass

    @abc.abstractmethod
    def get_dependency(self):
        """Returns a dependency object for this operation."""
        tpass