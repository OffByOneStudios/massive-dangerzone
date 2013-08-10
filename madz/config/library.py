"""config/library.py
@OffbyOne Studios 2013
Manages the configuration of libraries.
"""
from .base import *

#
# Config
#

class LibraryConfig(BaseConfig):
    """This represents the configuration for a library."""
    def __init__(self, library_name, options):
        self.library_name = library_name
        BaseConfig.__init__(self, options)

    @classmethod
    def make_key(cls, library_name):
        return (cls, library_name)

    def get_key(self):
        return self.make_key(self.library_name)

    def _str_view(self):
        return "Library Config for '{}'".format(self.library_name)


#
# Options
#

class OptionLibraryHeaderDirectories(BaseAppendOption): pass
class OptionLibraryLibraryDirectories(BaseAppendOption): pass
class OptionLibraryStaticLinkObjectFilenames(BaseAppendOption): pass
class OptionLibraryDynamicLinkStaticObjectFilenames(BaseAppendOption): pass
class OptionLibraryDynamicLinkDynamicObjectFilenames(BaseAppendOption): pass

