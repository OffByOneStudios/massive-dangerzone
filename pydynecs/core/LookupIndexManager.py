"""pydynecs/core/LookupComponentIndex.py
@OffbyOne Studios 2014
A dictionary based dynamic index manager.
"""
import abc

from .. import abstract

class LookupIndexManager(abstract.IIndexManager):
    def __init__(self, manager):
        if not(isinstance(manager, abstract.IObservableEntityManager)):
            raise Exception("Can only provide a lookup entity manager for observable managers.")
        self.manager = manager
        
        self._dict = {}
        self._dependencies = [manager]
        
        manager.on_mod().attach(self._on_mod)
        manager.on_des().attach(self._on_des)
        items = manager.items()
        for entity, value in items:
            self._update_index(entity, value)
    
    def dependencies(self):
        return list(map(lambda t: (t, {}), self._dependencies))
    
    @abc.abstractmethod
    def key(self, entity):
        """User defined function which provides a key given an entity."""
        pass
    
    def _update_index(self, entity):
        key = self.key(entity)
        if not (key is None):
            self._dict[key] = entity
    
    def _remove_index(self, entity):
        key = self.key(entity)
        if not (key is None):
            del self._dict[key]
    
    def _on_mod(self, manager, entity, isnew, expired):
        self._update_index(entity)

    def _on_des(self, manager, entity, isnew, expired):
        self._remove_index(entity)
        
    def get(self, key):
        return self._dict[key]
    
    def has(self, key):
        return key in self._dict
    
    def has_entity(self, entity):
        return entity in self._dict.values()
    
    def entities(self):
        return self._dict.values()
    
    def keys(self):
        return self._dict.keys()
    
    def items(self):
        return self._dict.items()
    
