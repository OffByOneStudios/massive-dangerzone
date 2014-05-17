
import pyext

from .. import abstract
from . import SimplePyAllocator

class System(abstract.ISystem, metaclass=pyext.ContextMetaGen(abstract.ISystem.__class__)):
    __pyext_context_base__ = True

    def __init__(self, allocator=None):
        if (allocator is None):
            self._allocator = SimplePyAllocator.SimplePyAllocator()
        elif (isinstance(allocator, abstract.IEntityAllocator)):
            self._allocator = allocator
        else:
            raise Exception("allocator: not a valid IEntityAllocator for system.")
    
        self._managers = {}
        self._indicies = {}
    
    def new_entity(self, *args, **kwargs): return self._allocator.new_entity(*args, **kwargs)
    def last_entity(self, *args, **kwargs): return self._allocator.last_entity(*args, **kwargs)
    def valid_entity(self, *args, **kwargs): return self._allocator.valid_entity(*args, **kwargs)
    def reclaim_entity(self, *args, **kwargs): return self._allocator.reclaim_entity(*args, **kwargs)

    def get_manager(self, key):
        return self._managers[key]
    
    def add_manager(self, key, manager):
        if key in self._managers:
            raise Exception("key: a manager already associated with key '{}'.".format(key))
        self._managers[key] = manager
        return manager
    
    def managers(self):
        return self._managers.items()

    def get_index(self, key):
        return self._indicies[key]
    
    def add_index(self, key, index):
        if key in self._indicies:
            raise Exception("key: an index already associated with key '{}'.".format(key))
        self._indicies[key] = index
        return index
    
    def indicies(self):
        return self._indicies.items()