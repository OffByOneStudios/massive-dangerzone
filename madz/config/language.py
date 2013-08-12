"""config/language.py
@OffbyOne Studios 2013
Manages the configuration of languages.
"""
import abc

from .base import *

#
# Config
#

class LanguageConfig(BaseLabeledConfig):
    """This represents the configuration for a language."""
    pass
    
#
# Options
#

class OptionLanguageCompilerPreference(BaseOption): pass
