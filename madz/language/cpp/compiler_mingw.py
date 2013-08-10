
import os

from ..c.compiler_mingw import MinGWCompiler as CMinGWCompiler

class MinGWCompiler(CMinGWCompiler):
    def binary_name_binary_compiler(self):
        return "g++"
