
import os

from .compiler_gcc import GCCCompiler

class MinGWCompiler(GCCCompiler):
    def __init__(self, language):
        GCCCompiler.__init__(self, language)

    def _gcc_visibility(self):
        return []

    def _gcc_shared_codegen(self):
        return []

    def _gcc_warn_unresolved(self):
        return []

    def args_link(self, object_files):
        return GCCCompiler.args_link(self, object_files) + ['-llibpthreadGC2'] #TODO, fix hack
