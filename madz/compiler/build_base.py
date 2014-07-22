"""subprocess_base.py
@Offbyone Studios 2014
"""
import logging
from abc import *

from .subprocess_base import SubprocessBase

logger = logging.getLogger(__name__)

class BuildBase(SubprocessBase):
    
    @abstractmethod
    def generate_compile_args(self, plugin_stub, language, compile_file):
        pass
    
    @abstractmethod
    def generate_link_args(self, plugin_stub, language, sourcefiles):
        pass
        
    def get_source_files(self, plugin_stub, language):
        source_files = language.get_source_files()
        source_files += language.get_internal_source_files()
        
        return source_files
        
    def build_plugin(self, plugin_stub, language):
        successful = True
        if not self.available:
            logger.error("Compiler '{}' Not Found".format(self.name))
            return False
            
        sourcefiles = self.get_source_files(plugin_stub, language)
        for compile_file in sourcefiles:
            sucsessful = successful and self.invoke("compile",
                dir=language.build_directory,
                args=self.generate_compile_args(plugin_stub, language, compile_file))
        
        sucsessful = successful and self.invoke("link",
            dir=language.build_directory,
            args=self.generate_link_args(plugin_stub, language, sourcefiles))
        
        return successful