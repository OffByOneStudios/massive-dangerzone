"""pydynecs/manager/EntityToComponentManager.py
@OffbyOne Studios 2014
Computes existence of entity on the fly.
"""
import abc

from .. import abstract
from .. import core

class EntityToComponentManager(abstract.IReadableComponentManager, abstract.IEntityManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actual_has_entity = self.has_entity
        self.has_entity = lambda e: True
    
    def get(self, entity):
        try:
            return self._actual_has_entity(entity)
        except:
            return False
    
    def values(self):
        return list(map(lambda e: True, self.entities))
    
    def items(self):
        return list(map(lambda e: (e, True), self.entities))