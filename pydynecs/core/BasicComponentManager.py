"""pydynecs/core/BasicComponentManager.py
@OffbyOne Studios 2014
A dictionary based dynamic component manager.
"""

from .. import abstract
from . import *

class BasicComponentManager(BaseManager, abstract.IComponentManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dict = {}
    
    def get(self, key):
        return self._dict[abstract.entity(key)]
    
    def set(self, key, value):
        self._dict[abstract.entity(key)] = value
    
    def des(self, key):
        del self._dict[abstract.entity(key)]
    
    def has_entity(self, key):
        return key in self._dict
    
    def entities(self):
        return list(self._dict.keys())
    
    def values(self):
        return list(self._dict.values())
    
    def items(self):
        return list(self._dict.items())
