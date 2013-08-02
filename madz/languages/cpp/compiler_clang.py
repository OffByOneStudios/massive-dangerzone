
import os

from ..c.compiler_clang import ClangCompiler as CClangCompiler

class ClangCompiler(CClangCompiler):
    def binary_name_binary_compiler(self):
        return "clang++"
