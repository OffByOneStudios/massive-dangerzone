"""pydynecs/core/System.py
@OffbyOne Studios 2014
Core system implementation.
"""
import abc

import pyext

from .. import abstract
from . import SimplePyAllocator

class SystemMeta(pyext.ContextMetaGen(type(abstract.ISystem))):
    def __init__(self, name, bases, attrs):
        self.__pyext_context_base__ = True
        super().__init__(name, bases, attrs)
        
        self._meta_manager_classes = {}
        self._meta_properties = []
        self._meta_property_lookup = {}
        self._meta_components = []
        self._meta_component_lookup = {}

class System(abstract.ISystem, metaclass=SystemMeta):
    def __init__(self, allocator=None):
        if (allocator is None):
            self._allocator = SimplePyAllocator.SimplePyAllocator(self)
        elif (isinstance(allocator, abstract.IEntityAllocator)):
            self._allocator = allocator
        else:
            raise Exception("allocator: not a valid IEntityAllocator for system.")
        
        self._managers = {}
        for (k, v) in self._meta_manager_classes.items():
            self._managers[k] = v(self)
    
    def new_entity(self, *args, **kwargs): return self.Entity(self._allocator.new_entity(*args, **kwargs))
    def last_entity(self, *args, **kwargs): return self.Entity(self._allocator.last_entity(*args, **kwargs))
    def valid_entity(self, *args, **kwargs): return self._allocator.valid_entity(*args, **kwargs)
    def reclaim_entity(self, *args, **kwargs): return self._allocator.reclaim_entity(*args, **kwargs)
    
    @classmethod
    def add_manager(cls, key, manager_class):
        meta = manager_class.meta()
        
        key = abstract.manager_key(key)
        if key in cls._meta_manager_classes:
            raise Exception("key: a manager already associated with key '{}'.".format(key))
        cls._meta_manager_classes[key] = manager_class
        
        if issubclass(manager_class, abstract.IEntityClass):
            for property in manager_class.properties():
                cls._add_property(key, manager_class, property)
        cls._add_component(key, manager_class, meta["component_name"] if "component_name" in meta else key)
        
        if not (cls.current is None):
            cls.current._managers[key] = manager_class(cls.current)
        return manager_class

    def get_manager(self, key):
        return self._managers[abstract.manager_key(key)]
    
    def managers(self):
        return self._managers.items()

    @classmethod
    def _add_property(self, key, manager_class, property):
        (property, meta) = property
        self._meta_properties.append((key, property, meta))
        property_name = meta["property_name"]
        if not (property_name in self._meta_property_lookup):
            self._meta_property_lookup[property_name] = []
        self._meta_property_lookup[property_name].append((key, property, meta))
        
    @classmethod
    def _add_component(self, key, manager_class, name):
        self._meta_components.append((name, key))
        self._meta_component_lookup[name] = key

    def has_component(self, _name, _entity, _check_set=False):
        return (_name in self._meta_component_lookup 
            and _entity in self._managers[self._meta_component_lookup[_name]]
            and (not _check_set or issubclass(self._meta_component_lookup[_name], abstract.IComponentManager)))
        
    def get_component(self, _name):
        return self._managers[self._meta_component_lookup[_name]]

    def has_property(self, _name, _entity):
        return (_name in self._meta_property_lookup
            and any(map(lambda p: self._managers[p[0]].has_entity(_entity),
                self._meta_property_lookup[_name])))
        
    def get_property(self, _name, _entity, *args, **kwargs):
        for (manager_class, prop, meta) in self._meta_property_lookup[_name]:
            if self._managers[manager_class].has_entity(_entity):
                return prop(self, _entity, *args, **kwargs)
        
    def __call__(self, entity):
        return self.Entity(entity)
        
    def __repr__(self):
        return "<EcsSystem: {}>".format(type(self).__qualname__)
    