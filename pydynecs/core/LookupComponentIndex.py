"""pydynecs/core/LookupComponentIndex.py
@OffbyOne Studios 2014
A dictionary based dynamic index manager.
"""

from .. import abstract

class LookupComponentIndex(abstract.IComponentIndex):
    def __init__(self, key_func):
        self._dict = {}
        self._key_func = key_func
    
    def _update_index(self, entity, value):
        self._dict[self._key_func(value)] = entity
    
    def attach(self, manager):
        for entity, value in manager.items():
            self._update_index(entity, value)
        def set(entity, value, _index=self, _pre_set=manager.set):
            _index._update_index(entity, value)
            _pre_set(entity, value)
        manager.set = set
    
    def get(self, key):
        return self._dict[key]
    
    def has(self, key):
        return key in self._dict
    
    def entities(self):
        return self._dict.values()
    
    def values(self):
        return self._dict.keys()
    
    def items(self):
        return self._dict.items()
    
