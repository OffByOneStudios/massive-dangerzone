"""pydynecs/core/CoercingComponentManager.py
@OffbyOne Studios 2014
A dictionary based typed component manager.
"""
import abc

from .. import abstract
from .BasicComponentManager import BasicComponentManager

class CoercingComponentManager(BasicComponentManager):
    def __init__(self):
        super().__init__()
    
    @abc.abstractmethod
    def coerce(self, value):
        pass
    
    def set(self, key, value):
        v = self.coerce(value)
        super().set(key, v)
