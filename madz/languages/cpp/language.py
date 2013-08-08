"""language.py
@OffbyoneStudios 2013
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob
import re

from .._base import language
from . import clean
from . import load
from . import compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguageCPP(language.BaseLanguage):
    compilers = {
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": compiler_mingw.MinGWCompiler,
        "clang": compiler_clang.ClangCompiler,
        "cl": compiler_cl.MSCLCompiler,
    }

    def get_compiler(self):
        compiler_config_list = self.plugin_stub.language_config.get_config_list("compiler")
        return self.compilers[compiler_config_list[0]](self, {})

    def make_cleaner(self):
        return clean.Cleaner(self)

    def make_loader(self):
        return load.Loader(self)

    def make_builder(self):
        return self.get_compiler()

    def make_wraper(self):
        return wrapgen.WrapperGenerator(self)

    def get_default_language_config(self):
        return {
            "compiler": "gcc",
            "compiler+unix": "gcc",
            "compiler+windows": "cl",
            "libs": [],
        }

    def get_wrap_directory(self):
        return os.path.join(self.plugin_stub.abs_directory, ".wrap-cpp")

    def get_build_directory(self):
        return os.path.join(self.plugin_stub.abs_directory, ".build-cpp")

    def get_cpp_header_filename(self):
        return os.path.join(self.get_wrap_directory(), "madz.h")

    def get_cpp_code_filename(self):
        return os.path.join(self.get_wrap_directory(), "_madz.cpp")

    def get_internal_source_files(self):
        return [self.get_cpp_code_filename()]

    def get_source_files(self):
        glob_pattern = os.path.join(self.plugin_stub.abs_directory, "*.cpp")

        # replace the left square bracket with [[]
        glob_pattern = re.sub(r'\[', '[[]', glob_pattern)
        # replace the right square bracket with []] but be careful not to replace
        # the right square brackets in the left square bracket's 'escape' sequence.
        glob_pattern = re.sub(r'(?<!\[)\]', '[]]', glob_pattern)

        return glob.glob(glob_pattern)

