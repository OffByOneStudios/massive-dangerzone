
import os

from ..c.compiler_gcc import GCCCompiler as CGCCCompiler

class GCCCompiler(CGCCCompiler):
    def binary_name_binary_compiler(self):
        return "g++"
