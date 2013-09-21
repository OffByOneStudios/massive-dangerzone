
import os
import logging

from ...config import *
from .._base import subproc_compiler as base

logger = logging.getLogger(__name__)

class MSCLCompiler(base.SubprocCompilerBase):
    """Compiler object for CL."""
    def __init__(self, language):
        base.SubprocCompilerBase.__init__(self, language)

    def file_extension_binary_object(self):
        """Returns the final extension for binary objects compiled by CL."""
        return ".obj"

    def binary_name_binary_compiler(self):
        """Returns the name of the compiler."""
        return "cl"

    def binary_name_shared_linker(self):
        """Returns the name of the shared linker."""
        return "LINK"

    def _gen_header_include_dirs(self):
        """Returns a list of the header include directories."""
        return map(lambda d: '/I"{}"'.format(d), self.config.get(OptionHeaderSearchPaths, []))

    def _gen_link_library_dirs(self):
        """Returns a list of the linked library directories."""
        return map(lambda d: "/LIBPATH:{}".format(d), self.config.get(OptionLibrarySearchPaths, []))
        
    def _gen_link_library_statics(self):
        return map(lambda d: '{}'.format(d), self.config.get(OptionLibraryStaticLinks, []))    
        
    def _gen_compile_flags(self):
        """Returns a list of compiler flags."""
        # We don't use optimization flags for cl. It is self optimizing /snark.
        return \
            (["/DEBUG:Yes"] if self.config.get(OptionCompilerDebug, False) else [])

    def _gen_link_flags(self):
        """Returns a list of linking flags."""
        return []

    def args_binary_compile(self, source_files):
        """Returns the complete list of arguments for compilation.
        
        Output Order:
            Compiler name -> compiler flags -> wrapper directory -> header include directories -> source files.
        """
        return [self.binary_name_binary_compiler(), "/c"] +\
            list(self._gen_compile_flags()) + \
            ["/I"+self.language.get_wrap_directory(),] + \
            list(self._gen_header_include_dirs()) + \
            list(source_files)

    def args_shared_link(self, object_files):
        """Returns the complete list of arguments for linking.
        
        Output Order:
            Linker name -> linker flags -> output file name -> linker library directories -> object files.
        """
        return [self.binary_name_shared_linker(), "/DLL "] +\
            list(self._gen_link_flags()) + \
            ["/OUT:"+self.language.get_output_file()] + \
            list(self._gen_link_library_dirs()) + \
            list(self._gen_link_library_statics()) + \
            list(object_files)

    def log_output(self, retcode, output, errput, foutput, ferrput):
        #TODO(Mason): Make the retcode do something, add proper description to function.
        """Logs output from compilation/linking to the logging system.
        
        Args:
            retcode: ???
            output:
            errput:
            foutput: 
            ferrput:
        """
        if output.find("error") != -1:
            logger.error(foutput)
        if errput.find("cl : Command line warning") != -1:
            logger.warning(ferrput)


