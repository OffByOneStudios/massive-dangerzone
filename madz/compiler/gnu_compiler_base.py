"""gnu_compiler_base.py
@Offbyone Studios 2014"""

from abc import *

from ..config import *

from .build_base import BuildBase



class GnuCompilerBase(BuildBase):

    @classmethod
    def _gen_header_include_dirs(cls, formatstring="-I{}"):
        """Returns a list of the header include directories."""
        return map(lambda d: formatstring.format(d), config.get(OptionHeaderSearchPaths, []))

    @classmethod
    def _gen_link_library_dirs(cls, formatstring="-L{}"):
        """Returns a list of the linked library directories."""
        return map(lambda d: formatstring.format(d), config.get(OptionLibrarySearchPaths, []))

    @classmethod
    def _format_static_library(cls, libname):
        return libname

    @classmethod
    def _gen_link_library_statics(cls, formatstring="-l{}"):
        """Returns a list of the linked library statics."""
        return map(
            lambda d: formatstring.format(cls._format_static_library(d)),
            config.get(OptionLibraryStaticLinks, []))

    @abstractmethod
    def binaryname_compiler(self, plugin_stub, language):
        pass

    def compiler_flags_base(self, plugin_stub, language):
        pass

    def compiler_flags_file(self, plugin_stub, language, compile_file):
        pass

    @abstractmethod
    def binaryname_linker(self, plugin_stub, language):
        pass

    def linker_flags_base(self, plugin_stub, language):
        pass

    def linker_flags_files(self, plugin_stub, language, source_files):
        pass

    def linker_flags_libraries(self, plugin_stub, language):
        pass

    def generate_compile_args(self, plugin_stub, language, compile_file):
        return [self.binaryname_compiler(plugin_stub, language)] \
            + list(self.compiler_flags_base(plugin_stub, language)) \
            + list(self.compiler_flags_file(plugin_stub, language, compile_file))

    def generate_link_args(self, plugin_stub, language, sourcefiles):
        return [self.binaryname_linker(plugin_stub, language)] \
            + list(self.linker_flags_base(plugin_stub, language)) \
            + list(self.linker_flags_files(plugin_stub, language, sourcefiles)) \
            + list(self.linker_flags_libraries(plugin_stub, language))

