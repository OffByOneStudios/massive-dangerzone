
import os

class MinGWCompiler(object):
    def __init__(self, language):
        self.language = language

    def object_file_extension(self):
        return ".o"

    def binary_name_compiler(self):
        return "gcc"

    def binary_name_linker(self):
        return self.binary_name_compiler()

    def args_compile(self, source_files):
        return [self.binary_name_compiler(), "-c", "-I"+self.language.get_wrap_directory()] + list(source_files)

    def args_link(self, object_files):
        return [self.binary_name_linker(), "-shared", "-o", self.language.get_output_file()] + list(object_files) + ['-llibpthreadGC2'] #T

    def log_output(self, logger, retcode, output, errput, foutput, ferrput):
        if retcode != 0:
            if output != "":
                logger.error(foutput)
            if errput != "":
                logger.error(ferrput)
        else:
            if output != "":
                logger.warning(foutput)
            if errput != "":
                logger.warning(ferrput)