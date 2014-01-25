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
from .._base import language
from .._base.compiler import NewCompilerWrapper
from . import clean
from . import load
from . import compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguageC(language.BaseLanguage):
    """Language object for C.s"""

    compilers = {
        """List of compatible compilers with C and MADZ."""
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": NewCompilerWrapper(mingw_compiler.MingwCompiler),
        "clang": compiler_clang.ClangCompiler,
        "cl": NewCompilerWrapper(cl_compiler.ClCompiler),
    }
    default_compiler = "gcc"

    def get_language_name(self):
        """Returns the name of the language."""
        return "c"

    def make_cleaner(self):
        """Creates the cleaner object."""
        return clean.Cleaner(self)

    def make_loader(self):
        """Creates the loader object."""
        return load.Loader(self)

    def make_builder(self):
        """Creates the builder object."""
        return self.get_compiler()

    def make_wrapper(self):
        """Creates the wrapper object."""
        return wrapgen.WrapperGenerator(self)

    def get_wrap_directory(self):
        """Returns the directory of the wrapper."""
        return os.path.join(self.plugin_stub.directory, ".wrap-c")

    def get_build_directory(self):
        """Returns the directory of the builder."""
        return os.path.join(self.plugin_stub.directory, ".build-c")

    def get_c_header_filename(self):
        """Returns the path to the filename of the madz header."""
        return os.path.join(self.get_wrap_directory(), "madz.h")

    def get_c_code_filename(self):
        """Returns the path to the filename of the c code."""
        return os.path.join(self.get_wrap_directory(), "_madz.c")

    def get_internal_source_files(self):
        """Returns a list of the internal c source files."""
        return [self.get_c_code_filename()]

    def get_source_files(self):
        #TODO(Mason): Add proper description to this method.
        """???"""
        glob_pattern = os.path.join(self.plugin_stub.directory, "*.c")

        # replace the left square bracket with [[]
        glob_pattern = re.sub(r'\[', '[[]', glob_pattern)
        # replace the right square bracket with []] but be careful not to replace
        # the right square brackets in the left square bracket's 'escape' sequence.
        glob_pattern = re.sub(r'(?<!\[)\]', '[]]', glob_pattern)

        return glob.glob(glob_pattern)

