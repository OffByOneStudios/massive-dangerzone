"""madzmodule:module/new/language/core/bootstrap.py
@OffbyOne Studios 2014
Interface for generating new language files.
"""

import abc

class INewLanguage(metaclass=abc.ABCMeta):
    """Abstract class for generating new language files"""


    @abc.abstractmethod
    def newlanguage_generate(self, **kwargs):
        """Perform this module operation."""
        pass

    @classmethod
    @abc.abstractmethod
    def newlanguage_identity(self):
        pass

    @classmethod
    @abc.abstractmethod
    def newlanguage_extension(self):
        pass
