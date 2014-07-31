"""pyext/core/EntityFacade.py
@OffbyOne Studios 2014
A useful abstraction to automatically use component managers like they were part of the entity object.
"""

import functools
import itertools

from .. import abstract

class EntityFacade(abstract.IEntity):
    """Pretends to be an entity in an object form."""
    
    @classmethod
    def _get_current_system(cls):
        return abstract.ISystem.current
    
    @property
    def system(self):
        return self._get_current_system()
    
    def __init__(self, entity=None):
        if (entity is None):
            self.__entity = abstract.entity(self.system.new_entity())
        elif (self.system.valid_entity(entity)):
            self.__entity = abstract.entity(entity)
        else:
            raise Exception("entity: not a valid IEntity for system.")
        
    def entity_id(self):
        return self.__entity

    def __getitem__(self, key):
        comp = self.system.get_manager(key)
        if isinstance(comp, abstract.IReadableComponentManager):
            return comp.get(self)
        else:
            return comp.has_entity(self)

    def __setitem__(self, key, value):
        comp = self.system.get_manager(key)
        comp.set(self, value)

    def __delitem__(self, key, value):
        comp = self.system.get_manager(key)
        comp.des(self)

    def __contains__(self, item):
        comp = self.system.get_manager(item)
        if isinstance(comp, abstract.IReadableComponentManager):
            return comp.has(self)
        else:
            return comp.has_entity(self)
        
    def __getattr__(self, key):
        if key.startswith("_"):
            return super().__getattr__(key, value)
        if self.system.has_component(key, self):
            return self.system.get_component(key)[self]
        elif self.system.has_property(key, self):
            return functools.partial(self.system.get_property, key, self)
        else:
            raise AttributeError("Entity does not have valid component or property for '{}'".format(key))
    
    def __setattr__(self, key, value):
        if key.startswith("_"):
            return super().__setattr__(key, value)
        if self.system.has_component(key, self, True):
            self.system.get_component(key)[self] = value
        else:
            raise AttributeError("Entity does not have valid component for '{}'".format(key))

    def __dir__(self):
        base = super().__dir__()
        baseset = set(base)
        base.extend(filter(lambda k: not (k in baseset), 
            itertools.chain(
                filter(lambda k: self.system.has_component(k, self), self.system.list_components()),
                filter(lambda k: self.system.has_property(k, self), self.system.list_properties()))))
        return base

    def __iter__(self):
        return iter(self.system.managers_of(self))

    def __len__(self):
        return len(self.system.managers_of(self))

    def items(self):
        return self.system.components_of(self)

    def __repr__(self):
        return "<EntityFacade: {} | {} components>".format(self.entity_id(), len(self))
