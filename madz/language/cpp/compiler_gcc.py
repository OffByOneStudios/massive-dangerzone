
import os

from ..c.compiler_gcc import GCCCompiler as CGCCCompiler

class GCCCompiler(CGCCCompiler):
    def _gen_specifc_compile_flags(self):
        return []
        
    def binary_name_binary_compiler(self):
        return "g++"

    def _gen_specifc_compile_flags(self):
        """Returns a list of the language specific compiler flags. Must be overloaded if a different language."""
        return \
            ["-std=c++11"]