import os
import logging

from ...config import *
from .._base import subproc_compiler as base

logger = logging.getLogger(__name__)

class GCCCompiler(base.SubprocCompilerBase):
    def __init__(self, language):
        base.SubprocCompilerBase.__init__(self, language)

    def file_extension_binary_object(self):
        return ".o"

    def binary_name_binary_compiler(self):
        return "gcc"

    def binary_name_shared_linker(self):
        return self.binary_name_binary_compiler()

    def _gen_header_include_dirs(self):
        return map(lambda d: "-I{}".format(d), self.config.get(OptionHeaderSearchPaths, []))

    def _gen_link_library_dirs(self):
        return map(lambda d: "-L{}".format(d), self.config.get(OptionLibrarySearchPaths, []))

    def _gen_link_library_statics(self):
        return map(lambda d: "-l{}".format(d), self.config.get(OptionLibraryStaticLinks, []))

    def _gcc_visibility(self):
        return ["-fvisibility=hidden"]

    def _gcc_shared_codegen(self):
        return ["-fpic"]

    def _gcc_warn_unresolved(self):
        return ["-Wl,-z,defs", "-Wl,--warn-unresolved-symbols"]

    def args_binary_compile(self, source_file):
        return [self.binary_name_binary_compiler(), "-c", "-I"+self.language.get_wrap_directory()] + \
            list(self._gen_header_include_dirs()) + \
            list(self._gcc_visibility()) + \
            list(self._gcc_shared_codegen()) + \
            list(source_file)

    def args_shared_link(self, object_files):
        return [self.binary_name_shared_linker(), "-shared", "-o", self.language.get_output_file()] + \
            list(self._gen_link_library_dirs()) + \
            list(self._gen_link_library_statics()) + \
            list(self._gcc_warn_unresolved()) + \
            list(object_files)

    def log_output(self, retcode, output, errput, foutput, ferrput):
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

