"""config/library.py
@OffbyOne Studios 2013
Manages the configuration of libraries.
"""
from .base import *

#
# Config
#

class LibraryConfig(BaseLabeledConfig):
    """This represents the configuration for a library."""
    pass

#
# Options
#

class OptionLibraryHeaderDirectories(BaseAppendOption): pass
class OptionLibraryLibraryDirectories(BaseAppendOption): pass
class OptionLibraryStaticLinkObjectFilenames(BaseAppendOption): pass
class OptionLibraryDynamicLinkStaticObjectFilenames(BaseAppendOption): pass
class OptionLibraryDynamicLinkDynamicObjectFilenames(BaseAppendOption): pass

