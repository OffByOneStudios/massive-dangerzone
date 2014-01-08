
import os

from .compiler_gcc import GCCCompiler

class ClangCompiler(GCCCompiler):
    """Compiler object for the Clang compiler.
    
    Attributes:
        language: A language object
    """
    def __init__(self, language):
        GCCCompiler.__init__(self, language)

    def binary_name_binary_compiler(self):
        """Returns the name of the compiler."""
        return "clang"

    def _gcc_shared_codegen(self):
        #TODO(Mason): Add proper description.
        """???"""
        return ["-fPIC"]

    def _gcc_warn_unresolved(self):
        """Returns the flags for an unresolved warning."""
        return ["-Wl,--warn-unresolved-symbols"]

