"""language.py
@OffbyoneStudios 2013
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob
import re

from ...compiler import mingw_compiler
from ...compiler import cl_compiler
from ...config import *
from ...fileman import *

from .._base import language
from .._base.compiler import NewCompilerWrapper

from .clean import Cleaner
from .load import Loader
from .wrapgen import WrapperGenerator
from . import compiler_gcc, compiler_clang

class LanguageCPP(language.BaseLanguage):
    compilers = {
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": NewCompilerWrapper(mingw_compiler.MingwCompiler),
        "clang": compiler_clang.ClangCompiler,
        "cl": NewCompilerWrapper(cl_compiler.ClCompiler),
    }
    default_compiler = "gcc"

    def get_language_name(self):
        return "cpp"

    def make_cleaner(self):
        return Cleaner(self)

    def make_loader(self):
        return Loader(self)

    def make_builder(self):
        return self.get_compiler()

    def make_wrapper(self):
        return WrapperGenerator(self)

    @property
    def wrap_directory(self):
        """Returns the directory of the wrapper."""
        return contents_directory(self.plugin_stub.directory.madz.subdirectory("cpp", ".wrap-cpp"))

    @property
    def build_directory(self):
        """Returns the directory of the builder."""
        return contents_directory(self.plugin_stub.directory.madz.subdirectory("cpp", ".build-cpp"))

    def get_cpp_header_filename(self):
        """Returns the path to the filename of the madz header."""
        return self.wrap_directory.file("madz.h")

    def get_cpp_code_filename(self):
        """Returns the path to the filename of the c code."""
        return self.wrap_directory.file("_madz.cpp")

    def get_internal_source_files(self):
        return [self.get_cpp_code_filename()]

    def get_debug_files(self):
        """Returns a list of debug data files"""
        return self.build_directory.files(["pdb"])
        
    def get_source_files(self):
        return self.plugin_stub.directory.files(["cpp"])

