"""config/language.py
@OffbyOne Studios 2013
Manages the configuration of languages.
"""
import abc

from .base import *

#
# Config
#

class LanguageConfig(BaseConfig):
    """This represents the configuration for a language."""
    def __init__(self, language_name, options):
        self.language_name = language_name
        BaseConfig.__init__(self, options)

    @classmethod
    def make_key(cls, language_name):
        return (cls, language_name)

    def get_key(self):
        return self.make_key(self.language_name)

    def _str_view(self):
        return "Language Config for '{}'".format(self.language_name)


#
# Options
#

class OptionLanguageCompiler(BaseOption): pass
