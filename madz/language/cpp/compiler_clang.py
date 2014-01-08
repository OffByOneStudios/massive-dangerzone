
import os

from ..c.compiler_clang import ClangCompiler as CClangCompiler

class ClangCompiler(CClangCompiler):
    def _gen_specifc_compile_flags(self):
        return []
        
    def binary_name_binary_compiler(self):
        return "clang++"

    def _gen_specifc_compile_flags(self):
        """Returns a list of the language specific compiler flags. Must be overloaded if a different language."""
        return \
            ["-std=c++11"]