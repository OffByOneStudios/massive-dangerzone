"""pydynecs/core/LookupComponentIndex.py
@OffbyOne Studios 2014
A dictionary based dynamic index manager.
"""
import abc

from .. import abstract

class LookupComponentIndex(abstract.IComponentIndex):
    def __init__(self, manager):
        self._dict = {}
        self._attach(manager)
    
    @abc.abstractmethod
    def key(self, value):
        pass
    
    def _update_index(self, entity, value):
        key = self.key(value)
        if not (key is None):
            self._dict[key] = entity
    
    def _attach(self, manager):
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
    
