
import os

from madz.languages.c import compiler_gcc as c_gcc

class GCCCompiler(c_gcc.GCCCompiler):
    def __init__(self, language):
        self.language = language

    def binary_name_compiler(self):
        return "g++"

    def binary_name_linker(self):
        return self.binary_name_compiler()

    def args_compile(self, source_file):
        return [self.binary_name_compiler(), "-c", "-I"+self.language.get_wrap_directory(), "-fvisibility=hidden", "-fpic"] + source_file

    def args_link(self, object_files):
        return [self.binary_name_linker(), "-shared", "-o", self.language.get_output_file()] + list(object_files) + ["-Wl,-z,defs"]
