
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
        self._properties = []
        self._property_lookup = {}
        self._components = []
        self._component_lookup = {}
    
    def new_entity(self, *args, **kwargs): return self.Entity(self._allocator.new_entity(*args, **kwargs))
    def last_entity(self, *args, **kwargs): return self.Entity(self._allocator.last_entity(*args, **kwargs))
    def valid_entity(self, *args, **kwargs): return self._allocator.valid_entity(*args, **kwargs)
    def reclaim_entity(self, *args, **kwargs): return self._allocator.reclaim_entity(*args, **kwargs)

    def get_manager(self, key):
        return self._managers[abstract.manager_key(key)]
    
    def add_manager(self, key, manager):
        meta = manager.meta()
        
        key = abstract.manager_key(key)
        if key in self._managers:
            raise Exception("key: a manager already associated with key '{}'.".format(key))
        self._managers[key] = manager
        
        if isinstance(manager, abstract.IEntityClass):
            for property in manager.properties():
                self._add_property(manager, property)
        self._add_component(manager, meta["component_name"] if "component_name" in meta else key)
        return manager
    
    def managers(self):
        return self._managers.items()

    def _add_property(self, manager, property):
        self._properties.append((manager, property))
        property_name = property[1]["property_name"]
        if not (property_name in self._property_lookup):
            self._property_lookup[property_name] = []
        self._property_lookup[property_name].append((manager, property))
        
    def _add_component(self, manager, name):
        self._components.append((name, manager))
        self._component_lookup[name] = manager

    def has_component(self, _name, _entity, _check_set=False):
        return (_name in self._component_lookup 
            and _entity in self._component_lookup[_name] 
            and (not _check_set or isinstance(self._component_lookup[_name], abstract.IComponentManager)))
        
    def get_component(self, _name):
        return self._component_lookup[_name]

    def has_property(self, _name, _entity):
        return _name in self._property_lookup and any(map(lambda p: p[0].has_entity(_entity), self._property_lookup[_name]))
        
    def get_property(self, _name, _entity, *args, **kwargs):
        for (manager, (prop, meta)) in self._property_lookup[_name]:
            if manager.has_entity(_entity):
                return prop(self, _entity, *args, **kwargs)
        
    def __call__(self, entity):
        return self.Entity(entity)