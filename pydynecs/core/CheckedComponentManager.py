"""pydynecs/core/TypedComponentManager.py
@OffbyOne Studios 2014
A dictionary based typed component manager.
"""
import abc

from .. import abstract
from .BasicComponentManager import BasicComponentManager

class CheckedComponentManager(BasicComponentManager):
    class CheckError(Exception): pass
    def __init__(self):
        super().__init__()
    
    @abc.abstractmethod
    def check(self, value):
        pass
        
    def set(self, key, value):
        if not self.check(value):
            raise CheckedComponentManager.CheckError()
        super().set(key, value)
