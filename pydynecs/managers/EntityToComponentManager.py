"""pydynecs/manager/EntityToComponentManager.py
@OffbyOne Studios 2014
Computes existence of entity on the fly.
"""
import abc

from .. import abstract
from .. import core

class EntityToComponentManager(abstract.IReadableComponentManager, abstract.IEntityManager):
    def get(self, entity):
        return self.has_entity(entity)
    
    def values(self):
        return list(map(lambda e: True, self.entities))
    
    def items(self):
        return list(map(lambda e: (e, True), self.entities))