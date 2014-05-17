"""pydynecs/core/CoercingComponentManager.py
@OffbyOne Studios 2014
A dictionary based typed component manager.
"""

from .. import abstract
from .BasicComponentManager import BasicComponentManager

class CoercingComponentManager(BasicComponentManager):
    def __init__(self, coerce):
        super().__init__()
        self.coerce = coerce
    
    def set(self, key, value):
        v = self.coerce(value)
        super().set(key, v)
