"""language.py
@OffbyoneStudios 2013
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob
import re

from ...compiler import mingw_compiler, cl_compiler, clang_compiler
from ...config import *
from ...fileman import *

from .._base import language
from .._base.compiler import NewCompilerWrapper

from . import clean
from . import compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguageC(language.BaseLanguage):
    """Language object for C.s"""

    compilers = {
        """List of compatible compilers with C and MADZ."""
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": NewCompilerWrapper(mingw_compiler.MingwCompiler),
        "clang": NewCompilerWrapper(clang_compiler.ClangCompiler),
        "cl": NewCompilerWrapper(cl_compiler.ClCompiler),
    }
    default_compiler = "gcc"

    def get_language_name(self):
        """Returns the name of the language."""
        return "c"

    def make_cleaner(self):
        """Creates the cleaner object."""
        return clean.Cleaner(self)

    def make_builder(self):
        """Creates the builder object."""
        return self.get_compiler()

    def make_wrapper(self):
        """Creates the wrapper object."""
        return wrapgen.WrapperGenerator(self)

    @property
    def wrap_directory(self):
        """Returns the directory of the wrapper."""
        return self.plugin_stub.directory.madz().dir("c", ".wrap-c")

    @property
    def build_directory(self):
        """Returns the directory of the builder."""
        return self.plugin_stub.directory.madz().dir("c", ".build-c")

    def get_c_header_filename(self):
        """Returns the path to the filename of the madz header."""
        return self.wrap_directory.file("madz.h")

    def get_c_code_filename(self):
        """Returns the path to the filename of the c code."""
        return self.wrap_directory.file("_madz.c")

    def get_internal_source_files(self):
        """Returns a list of the internal c source files."""
        return [self.get_c_code_filename()]

    def get_debug_files(self):
        """Returns a list of debug data files"""
        return self.build_directory.list(["pdb"])

    def get_source_files(self):
        return self.plugin_stub.directory.list(["c"])
