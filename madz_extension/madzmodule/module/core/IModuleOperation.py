"""madzmodule:module/core/IModuleOperation.py
@OffbyOne Studios 2014
Module Operation Interface
"""

import abc

class IModuleOperation(metaclass=abc.ABCMeta):
    """Abstract class for module operations"""


    @abc.abstractmethod
    def moduleoperation_perform(self, **kwargs):
        """Perform this module operation."""
        pass

    @classmethod
    @abc.abstractmethod
    def moduleoperation_identity(self):
        pass
