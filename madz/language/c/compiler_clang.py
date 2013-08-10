
import os

from .compiler_gcc import GCCCompiler

class ClangCompiler(GCCCompiler):
    def __init__(self, language, compiler_config):
        GCCCompiler.__init__(self, language, compiler_config)

    def binary_name_binary_compiler(self):
        return "clang"

    def _gcc_visibility(self):
        return ["-fvisibility=hidden"]

    def _gcc_shared_codegen(self):
        return ["-fPIC"]

    def _gcc_warn_unresolved(self):
        return ["-Wl,--warn-unresolved-symbols"]

