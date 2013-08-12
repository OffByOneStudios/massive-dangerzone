"""config/compiler.py
@OffbyOne Studios 2013
Manages the configuration of compilers.
"""
from .base import *

#
# Config
#

class CompilerConfig(BaseLabeledConfig):
    """This represents the configuration for a library."""
    pass

#
# Options
#

# Binary Libraries

class OptionLibrarySearchPaths(BaseAppendOption): pass
class OptionLibraryStaticLinks(BaseAppendOption): pass
class OptionLibraryDynamicLinks(BaseAppendOption): pass

# Source Headers

class OptionHeaderSearchPaths(BaseAppendOption): pass
class OptionHeaderIncludes(BaseAppendOption): pass
