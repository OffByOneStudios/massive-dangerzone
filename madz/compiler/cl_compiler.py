import os
import shutil

from .build_base import BuildBase

from ..config import *

class LogFilter(object):
    """Helper Class to trunticate Log output. It's So long!"""
    
    def __init__(self, string):
        self.string = string
    
    def format(self):
        pass
        
    def __str__(self):
        return self.format()

        
class IdentityLogFilter(LogFilter):
    """Log Filter which returns it's input"""
    
    def format(self):
        return self.string
        
class CLVerbosityLogFilter(LogFilter):
    """Helper Class to limit the amount of information returned from CL"""
    
    def format(self):
        import re
        
        fileRegex = "(^[^ \\/:*?""<>|]+([ ]+[^ \\/:*?""<>|]+)*$)"
        errorRegex = ": error C[0-9]+:"
        errorLines = self.string.split("\n")
        res = []
        for line in errorLines:
            match = re.search(errorRegex, line)
            if match != None:
                file, error = line.split(match.group(0))
                res.append("\t" + file[file.rfind("\\") + 1 : ] + ":" + error)
            else:
                res.append(line)
        return '\n'.join(res)
        
class ClCompiler(BuildBase):

    @property
    def name(self):
        return "cl"

    @property
    def supported_languages(self):
        return ["c", "cpp"]

    @property
    def available():
        try:
            ret, out, err = self.invoke_simple(["cl", "/help"])
            return ret == 0
        except:
            return False

    @classmethod
    def _format_static_library(cls, libname):
        return libname
        
    def sourcefile_to_objectfile(self, compile_file):
        return (".".join(os.path.basename(compile_file).split(".")[:-1])) + ".obj"
        
    @classmethod
    def _gen_header_include_dirs(cls, formatstring='/I{}'):
        """Returns a list of the header include directories."""
        return map(lambda d: formatstring.format(d), config.get(OptionHeaderSearchPaths, []))

    @classmethod
    def _gen_link_library_dirs(cls, formatstring="/LIBPATH:{}"):
        """Returns a list of the linked library directories."""
        return map(lambda d: formatstring.format(d), config.get(OptionLibrarySearchPaths, []))
    
    def _gen_link_library_statics(cls, formatstring="{}"):
        return map(lambda d: formatstring.format(d), config.get(OptionLibraryStaticLinks, []))
    
    def binaryname_compiler(self, plugin_stub, language):
        return {
            "c": "cl",
            "cpp": "cl",
        }[language.name]
    
    def compiler_flags_base(self, plugin_stub, language):
        return (
            #Debug Symbols
            #Use LINK Seperately
            (["/c"]) +
            # Include Directories
            ["/I"+language.get_wrap_directory()] + list(self._gen_header_include_dirs()) +
            # Warnings            
           (["/Zi", "/W4"] if config.get(OptionCompilerDebug, False) else []) 
        )

    def compiler_flags_file(self, plugin_stub, language, compile_file):
        return [str(compile_file)]
        
    def binaryname_linker(self, plugin_stub, language):
        return {
            "c": "LINK",
            "cpp": "LINK",
        }[language.name]

    def linker_flags_base(self, plugin_stub, language):
        return (
            # Basic Linker Flags
            (["/DEBUG"]) +
            (["/DLL"]) +
            
            # Library Directories
            list(self._gen_link_library_dirs()) 
            # Warnings
            )

    def linker_flags_files(self, plugin_stub, language, source_files):
        return ["/OUT:"+language.get_output_file()] + \
            list(map(self.sourcefile_to_objectfile, source_files)) 

    def linker_flags_libraries(self, plugin_stub, language):
        return (list(map(lambda m: "{}.lib".format(m), self._gen_link_library_statics())))
        
    def generate_compile_args(self, plugin_stub, language, compile_file):
        return [self.binaryname_compiler(plugin_stub, language)] \
            + list(self.compiler_flags_base(plugin_stub, language)) \
            + list(self.compiler_flags_file(plugin_stub, language, compile_file))

    def generate_link_args(self, plugin_stub, language, sourcefiles):
        return [self.binaryname_linker(plugin_stub, language)] \
            + list(self.linker_flags_base(plugin_stub, language)) \
            + list(self.linker_flags_files(plugin_stub, language, sourcefiles)) \
            + list(self.linker_flags_libraries(plugin_stub, language))
            
            
    def process_output(self, name, retcode, output, errput, foutput, ferrput):
        error = CLVerbosityLogFilter(foutput)
        if output.find("error") != -1:
            logger.error(error.format())
        if errput.find("cl : Command line warning") != -1:
            logger.warning(ferrput)

        return retcode == 0
        
    def build_plugin(self, plugin_stub, language):
        BuildBase.build_plugin(self, plugin_stub, language)
        for debug in language.get_debug_files():
            shutil.copyfile(debug,
                language.get_output_directory() + "/" + os.path.basename(debug))