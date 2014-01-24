"""compilerbase.py
@OffByOneStudios 2014
"""

from abc import *


class CompilerBase(metaclass=ABCMeta):
    """Abstract Base Class for Compilers"""
    
    @property
    @abstractmethod
    def name(self):
        pass
    
    @property
    @abstractmethod
    def supported_languages(self):
        pass
    
    @property
    @abstractmethod
    def available(self):
        """Tests if this compiler is available on system."""
        pass
    
    @abstractmethod
    def build_plugin(self, plugin_stub, language):
        pass
        