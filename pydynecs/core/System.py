
import pyext

from .. import abstract
from . import SimplePyAllocator

class System(abstract.ISystem, metaclass=pyext.ContextMetaGen(abstract.ISystem.__class__)):
    __pyext_context_base__ = True

    def __init__(self, allocator=None):
        if (allocator is None):
            self._allocator = SimplePyAllocator.SimplePyAllocator(type(self))
        elif (isinstance(allocator, abstract.IEntityAllocator)):
            self._allocator = allocator
        else:
            raise Exception("allocator: not a valid IEntityAllocator for system.")
    
        self._managers = {}
    
    def new_entity(self, *args, **kwargs): return self._allocator.new_entity(*args, **kwargs)
    def last_entity(self, *args, **kwargs): return self._allocator.last_entity(*args, **kwargs)
    def valid_entity(self, *args, **kwargs): return self._allocator.valid_entity(*args, **kwargs)
    def reclaim_entity(self, *args, **kwargs): return self._allocator.reclaim_entity(*args, **kwargs)

    def get_manager(self, key):
        return self._managers[abstract.manager_key(key)]
    
    def add_manager(self, key, manager):
        key = abstract.manager_key(key)
        if key in self._managers:
            raise Exception("key: a manager already associated with key '{}'.".format(key))
        self._managers[key] = manager
        return manager
    
    def managers(self):
        return self._managers.items()

    #def __getitem__(self, key):
    #    if self.valid_entity(key):
    #        return self.