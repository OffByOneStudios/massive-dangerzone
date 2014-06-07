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

# Compiler prefrence
class OptionCompilerPreference(BaseOption): pass

# Binary Libraries

class OptionLibrarySearchPaths(BaseAppendOption): pass
class OptionLibraryStaticLinks(BaseAppendOption): pass
class OptionLibraryDynamicLinks(BaseAppendOption): pass
class OptionLibraryFrameworks(BaseAppendOption): pass

# Source Headers

class OptionHeaderSearchPaths(BaseAppendOption): pass
class OptionHeaderIncludes(BaseAppendOption): pass

# Flags

class OptionCompilerDebug(BaseOption):
    default_value = False

# Optimization

class OptionCompilerOptimization(BaseOption):
    """A value between 0.0 and 1.0 inclusive representing how much optimization to attempt."""
    default_value = 1.0
