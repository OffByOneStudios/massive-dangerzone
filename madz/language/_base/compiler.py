import abc

from ...config import *

class BaseCompiler(object):
    """The base compiler object.
    
    Attributes:
        language: A BaseLanguage object.
        config: A MergedConfig object.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, language):
        self.language = language
        self.config = config.save()

    class BuildType():
        DynamicPlugin = 0
        StaticPlugin = 1

    @abc.abstractmethod
    def build(self, type=BuildType.DynamicPlugin):
        """Builds a plugin of the given type."""
        pass

    @abc.abstractmethod
    def get_dependency(self):
        """Returns a dependency object for this operation."""
        pass

    def do(self):
        self.build()

def NewCompilerWrapper(new_type)
    class NewCompilerWrapper_GEN(BaseCompiler):
        _new_type = new_type
        def __init__(self, *args, **kwargs):
            super().__init__(self, *args, **kwargs)
            self._new = self._new_type()
            
        def build(self):
            tmp_config = config
            try:
                config = self.config
                self._new.build_plugin(self.language.plugin_stub, self.language)
            finally:
                config = tmp_config
       
        def get_dependency(self):
            """Returns a dependency object for this operation."""
            return False       
    return NewCompilerWrapper_GEN
            

        