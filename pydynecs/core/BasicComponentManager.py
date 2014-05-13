"""pydynecs/core/BasicComponentManager.py
@OffbyOne Studios 2014
A dictionary based dynamic component manager.
"""

from .. import abstract

class BasicComponentManager(abstract.IComponentManager):
    def __init__(self):
        self._dict = {}
    
    def get(self, key):
        return self._dict[key]
    
    def set(self, key, value):
        self._dict[key] = value
    
    def des(self, key):
        del self._dict[key]
    
    def has(self, key):
        return key in self._dict
    
    def entities(self):
        return self._dict.keys()
    
    def values(self):
        return self._dict.values()
    
    def items(self):
        return self._dict.items()
    
