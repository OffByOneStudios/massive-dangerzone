"""language.py
@OffbyoneStudios 2013
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob
import re

from ...config import *
from .._base import language
from . import clean
from . import load
from . import compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguageC(language.BaseLanguage):
    compilers = {
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": compiler_mingw.MinGWCompiler,
        "clang": compiler_clang.ClangCompiler,
        "cl": compiler_cl.MSCLCompiler,
    }
    default_compiler = "gcc"

    def get_language_name(self):
        return "c"

    def make_cleaner(self):
        return clean.Cleaner(self)

    def make_loader(self):
        return load.Loader(self)

    def make_builder(self):
        return self.get_compiler()

    def make_wrapper(self):
        return wrapgen.WrapperGenerator(self)

    def get_wrap_directory(self):
        return os.path.join(self.plugin_stub.directory, ".wrap-c")

    def get_build_directory(self):
        return os.path.join(self.plugin_stub.directory, ".build-c")

    def get_c_header_filename(self):
        return os.path.join(self.get_wrap_directory(), "madz.h")

    def get_c_code_filename(self):
        return os.path.join(self.get_wrap_directory(), "_madz.c")

    def get_internal_source_files(self):
        return [self.get_c_code_filename()]

    def get_source_files(self):
        glob_pattern = os.path.join(self.plugin_stub.directory, "*.c")

        # replace the left square bracket with [[]
        glob_pattern = re.sub(r'\[', '[[]', glob_pattern)
        # replace the right square bracket with []] but be careful not to replace
        # the right square brackets in the left square bracket's 'escape' sequence.
        glob_pattern = re.sub(r'(?<!\[)\]', '[]]', glob_pattern)

        return glob.glob(glob_pattern)

