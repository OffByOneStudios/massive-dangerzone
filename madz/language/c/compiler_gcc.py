import os
import logging

from ...config import *
from .._base import subproc_compiler as base

logger = logging.getLogger(__name__)

class GCCCompiler(base.SubprocCompilerBase):
    """Compiler object for GCC.
    
    Attributes:
        language: Language object
    """
    def __init__(self, language):
        base.SubprocCompilerBase.__init__(self, language)

    def file_extension_binary_object(self):
        """Returns the file extension for binary objects of this compiler."""
        return ".o"

    def binary_name_binary_compiler(self):
        """Returns the name of the compiler."""
        return "gcc"

    def binary_name_shared_linker(self):
        """Returns the name of the shared linker."""
        return self.binary_name_binary_compiler()

    def _gen_header_include_dirs(self):
        """Returns a list of the header include directories."""
        return map(lambda d: "-I{}".format(d), self.config.get(OptionHeaderSearchPaths, []))

    def _gen_link_library_dirs(self):
        """Returns a list of the linked library directories."""
        return map(lambda d: "-L{}".format(d), self.config.get(OptionLibrarySearchPaths, []))

    def _gen_link_library_statics(self):
        """Returns a list of the linked library statistics."""
        return map(lambda d: "-l{}".format(d), self.config.get(OptionLibraryStaticLinks, []))

    def _gen_compile_flags(self):
        """Returns a list of the compiler flags."""
        return \
            (["-O0"] if (self.config.get(OptionCompilerDebug, 0.0) < 0.5) else ["-O4"]) + \
            (["-g"] if self.config.get(OptionCompilerDebug, False) else [])

    def _gen_link_flags(self):
        """Returns a list of the linker flags."""
        return []

    def _gcc_visibility(self):
        """Returns the visibility of the compiler."""
        return ["-fvisibility=hidden"]

    def _gcc_shared_codegen(self):
        #TODO(Mason): Add proper description to this method.
        """???"""
        return ["-fpic"]

    def _gcc_warn_unresolved(self):
        """Returns list of unresolved warnings."""
        return ["-Wl,-z,defs", "-Wl,--warn-unresolved-symbols"]

    def args_binary_compile(self, source_file):
        """Returns the complete list of arguments for compilation.
        
        Output Order:
            Compiler name -> compiler flags -> wrapper directory -> header include directories -> source files.
        """
        return [self.binary_name_binary_compiler()] + \
            list(self._gen_compile_flags()) + \
            ["-c", "-I"+self.language.get_wrap_directory()] + \
            list(self._gen_header_include_dirs()) + \
            list(self._gcc_visibility()) + \
            list(self._gcc_shared_codegen()) + \
            list(source_file)

    def args_shared_link(self, object_files):
        """Returns the complete list of arguments for linking.
        
        Output Order:
            Linker name -> linker flags -> output file name -> linker library directories -> object files.
        """
        return [self.binary_name_shared_linker(), "-shared"] + \
            list(self._gen_link_flags()) + \
            ["-o", self.language.get_output_file()] + \
            list(self._gen_link_library_dirs()) + \
            list(self._gcc_warn_unresolved()) + \
            list(object_files) + \
            list(self._gen_link_library_statics())

    def log_output(self, retcode, output, errput, foutput, ferrput):
        #TODO(Mason): Add proper description to function.
        """Logs output from compilation/linking to the logging system.
        
        Args:
            retcode: ???
            output:
            errput:
            foutput: 
            ferrput:
        """
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

