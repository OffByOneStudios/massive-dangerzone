
import os

class MSCLCompiler(object):
    def __init__(self, language):
        self.language = language

    def object_file_extension(self):
        return ".obj"

    def binary_name_compiler(self):
        return "cl"

    def binary_name_linker(self):
        return "LINK"

    def args_compile(self, source_files):
        #print ([self.binary_name_compiler(), "/c", "/I"+self.language.get_wrap_directory(),] + list(source_files))
        return [self.binary_name_compiler(), "/c", "/I"+self.language.get_wrap_directory(),] + list(source_files)# +["/link /out:"+self.language.get_output_file()]

    def args_link(self, object_files):
        return [self.binary_name_linker(), "/DLL ", "/OUT:"+self.language.get_output_file()] + list(object_files)

    def log_output(self, logger, retcode, output, errput, foutput, ferrput):

        if output.find("error") != -1:
            logger.error(foutput)
        if errput.find("cl : Command line warning") != -1:
            logger.warning(ferrput)


