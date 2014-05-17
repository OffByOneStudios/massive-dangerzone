"""pydynecs/core/TypedComponentManager.py
@OffbyOne Studios 2014
A dictionary based typed component manager.
"""

from .. import abstract
from .BasicComponentManager import BasicComponentManager

class CheckedComponentManager(BasicComponentManager):
    class CheckError(Exception): pass
    def __init__(self, type_check):
        super().__init__()
        self.check = type_check
    
    def set(self, key, value):
        if not self.check(value):
            raise CheckedComponentManager.CheckError()
        super().set(key, value)
