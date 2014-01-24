import abc

from ...config import *
from ...core.dependency import Dependency

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

def NewCompilerWrapper(new_type):
    global config
    class NewCompilerWrapper_GEN(BaseCompiler):
        _new_type = new_type
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._new = self._new_type()

        def build(self):
            global config
            tmp_config = config
            try:
                if not (os.path.exists(self.language.get_build_directory())):
                    os.makedirs(self.language.get_build_directory())

                if not (os.path.exists(self.language.get_output_directory())):
                    os.makedirs(self.language.get_output_directory())

                config = self.config
                self._new.build_plugin(self.language.plugin_stub, self.language)
            finally:
                config = tmp_config

        def get_dependency(self):
            """Returns a dependency object for this operation."""
            targets = [self.language.get_output_file()]
            dependencies = list(self.language.get_source_files())
            dependencies.extend(self.language.get_internal_source_files())
            return Dependency(dependencies, targets)

    return NewCompilerWrapper_GEN



