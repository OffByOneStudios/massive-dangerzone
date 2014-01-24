

from .gnu_compiler_base import GnuCompilerBase



class MingwCompiler(GnuCompilerBase):

    @property
    def name(self):
        return "mingw"
        
    @property
    def supported_languages(self):
        return ["c", "cpp"]
    
    @property
    def available(): 
        try:
            ret, out, err = self.invoke_simple(["gcc", "--version"])
            return ret == 0
        except:
            return False
            
    @classmethod
    def _format_static_library(cls, libname):
        if libname.endswith(".lib"):
            libname = libname[:-4]
        return libname
        
    def sourcefile_to_objectfile(self, compile_file):
        return ".".join(compile_file.split(".")[:-1] + ["o"])
        
    def binaryname_compiler(self, plugin_stub, language):
        return {
            "c": "gcc",
            "cpp": "g++",
        }[language.get_language_name()]
                   
    def compiler_flags_base(self, plugin_stub, language):
        return (
            # Basic Compiler Flags
            (["-O0"] if (self.config.get(OptionCompilerDebug, 0.0) < 0.5) else ["-O4"]) + 
            (["-g"] if self.config.get(OptionCompilerDebug, False) else []) + 
            # Language Compiler Flags
            ({ 
                "c": ["-std=c11", "-xc"],
                "cpp": ["-std=c++11", "-xc++"],
            }[language.get_language_name()]) + 
            # Include Directories
            ["-I"+self.language.get_wrap_directory()] + list(self._gen_header_include_dirs()) + 
            # Linker Prep (position independant code and visibility)
            ["-fvisibility=hidden", "-fpic"] + 
            # Warnings
            ["-Wall"])
    
    def compiler_flags_file(self, plugin_stub, language, compile_file):
        return ["-c", str(compile_file), "-o", self.sourcefile_to_objectfile(compile_file)]
    
    def binaryname_linker(self, plugin_stub, language):
        return self.binaryname_compiler(plugin_stub, language)
    
    def linker_flags_base(self, plugin_stub, language):
        return (
            # Basic Linker Flags
            ["-mwindows"] +
            # Language Linker Flags
            ({ 
                "c": [],
                "cpp": [],
            }[language.get_language_name()]) + 
            # Library Directories
            list(self._gen_link_library_dirs()) + 
            # Linker Prep (position independant code and visibility)
            ["-fvisibility=hidden", "-fpic"] + 
            # Warnings
            ["-Wl,-z,defs", "-Wl,--warn-unresolved-symbols"])
    
    def linker_flags_files(self, plugin_stub, language, source_files):
        return ["-o", self.language.get_output_file()] + \
            list(map(self.sourcefile_to_objectfile, source_files))
    
    def linker_flags_libraries(self, plugin_stub, language):
        return (list(self._gen_link_library_statics()) * 2)
    