"""pydynecs/core/LookupComponentIndex.py
@OffbyOne Studios 2014
A dictionary based dynamic index manager.
"""
import abc

from .. import abstract
from . import *

class LookupIndexManager(BaseManager, abstract.IIndexManager):
    source = None
    def __init__(self, *args, **kwargs):
        if self.source is None:
            raise Exception("Must have a source to build lookup on.")
            
        super().__init__(*args, **kwargs)
        
        self._source_manager = abstract.manager(self.get_system(), self.source)
        if not(isinstance(self._source_manager, abstract.IObservableEntityManager)):
            raise Exception("Can only provide a lookup index manager for observable source managers.")
        
        self._dict = {}
        
        self._source_manager.on_mod().attach(self._on_mod)
        self._source_manager.on_des().attach(self._on_des)
        items = self._source_manager.items()
        for entity, value in items:
            self._update_index(entity, value)
    
    def get_dependencies(self):
        return super().get_dependencies() + [self.source]
    
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
    
