
import os

class MinGWCompiler(object):
    def __init__(self, language):
        self.language = language

    def binary_name_compiler(self):
        return "g++"

    def binary_name_linker(self):
        return self.binary_name_compiler()

    def args_compile(self, source_files):
        return [self.binary_name_compiler(), "-c", "-I"+self.language.get_wrap_directory()] + source_files

    def args_link(self, object_files):
        return [self.binary_name_linker(), "-shared", "-o", self.language.get_output_file()] + object_files
