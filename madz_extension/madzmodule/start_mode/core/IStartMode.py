"""madzmodule:start_mode/core/IStartMode.py
@OffbyOne Studios 2014
Interface for module start modes
"""

import abc

class IStartMode(metaclass=abc.ABCMeta):
    """Abstract class for module start modes"""

    @classmethod
    @abc.abstractmethod
    def add_argparser(self, subparser):
        """Attach this object's parser to a subparser group"""
        pass

    @abc.abstractmethod
    def startmode_start(self, parsed_args):
        """Start this module sub-startmode

        Args:
            the result of calling parse on the argparser retrived from this class
        """
        pass

    @classmethod
    def startmode_identity(self):
        pass
