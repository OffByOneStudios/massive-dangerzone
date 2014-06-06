"""pydynecs/manager/ComputedEntityManager.py
@OffbyOne Studios 2014
Computes existence of entity on the fly.
"""
import abc

from .. import abstract
from .. import core

class ComputedEntityManager(core.BaseManager, abstract.IEntityManager):
    @abc.abstractmethod
    def compute(self, entity):
        pass
        
    def has_entity(self, entity):
        return self.dependencies_has_entity(entity) and self.compute(entity)
    
    def entities(self):
        # TODO, if observable, cache
        return list(filter(self.compute, self.dependencies()[0][0].entities()))
