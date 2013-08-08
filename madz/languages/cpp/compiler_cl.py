
import os

from ..c.compiler_cl import MSCLCompiler as CMSCLCompiler

class MSCLCompiler(CMSCLCompiler):
    def binary_name_compiler(self):
        return "cl"


