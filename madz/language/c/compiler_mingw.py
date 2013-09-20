
import os

from .compiler_gcc import GCCCompiler

class MinGWCompiler(GCCCompiler):
    """Compiler object for MinGW.
    
    Attributes:
        language: Language object.
    """
    def __init__(self, language):
        GCCCompiler.__init__(self, language)

    def _gcc_visibility(self):
        """Returns the visibility of the compiler."""
        return []

    def _gcc_shared_codegen(self):
        #TODO(Mason): Add proper description.
        """???"""
        return []

    def _gcc_warn_unresolved(self):
        """Returns list of unresolved warning flags."""
        return []
