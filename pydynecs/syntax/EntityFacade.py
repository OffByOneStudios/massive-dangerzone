"""pyext/syntax/EntityFacade.py
@OffbyOne Studios 2014
A useful abstraction to automatically use component managers like they were part of the entity object.
"""

from .. import abstract
from .exceptions import *

class EntityFacade(abstract.IEntity):
    """Pretends to be an entity in an object form."""
    @classmethod
    def _get_current_system(cls):
        return abstract.ISystem.current
    
    def __init__(self, entity=None, system=None):
        if (system is None):
            self.system = self._get_current_system()
        elif (isinstance(system, abstract.ISystem)):
            self.system = system
        else:
            raise EcsSyntaxArgumentError("system: not an ISystem.")

        if (entity is None):
            self.entity = abstract.entity(self.system.new_entity())
        elif (self.system.valid_entity(entity)):
            self.entity = abstract.entity(entity)
        else:
            raise EcsSyntaxArgumentError("entity: not a valid IEntity for system.")

    def entity_id(self):
        return self.entity

    def __getitem__(self, key):
        comp = self.system.get_manager(key)
        if comp is None:
            raise EcsSyntaxKeyError("'{}' is not a component of system.".format(key))

        return comp.get(self.entity)

    def __setitem__(self, key, value):
        comp = self.system.get_manager(key)
        if comp is None:
            raise EcsSyntaxKeyError("'{}' is not a component of system.".format(key))

        comp.set(self.entity, value)

    def __delitem__(self, key, value):
        comp = self.system.get_manager(key)
        if comp is None:
            raise EcsSyntaxKeyError("'{}' is not a component of system.".format(key))

        comp.des(self.entity)

    def __contains__(self, item):
        comp = self.system.get_manager(item)
        return comp.has(self.entity)

    def __iter__(self):
        return iter(self.system.managers_of(self.entity))

    def __len__(self):
        return len(self.system.managers_of(self.entity))

    def items(self):
        return self.system.components_of(self.entity)

    def __repr__(self):
        return "<EntityFacade: {} | {} components>".format(self.entity_id(), len(self))
