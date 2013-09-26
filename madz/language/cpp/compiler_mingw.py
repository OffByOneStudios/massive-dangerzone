
import os

from ..c.compiler_mingw import MinGWCompiler as CMinGWCompiler

class MinGWCompiler(CMinGWCompiler):
    def _gen_specifc_compile_flags(self):
        return []

    def binary_name_binary_compiler(self):
        return "g++"
