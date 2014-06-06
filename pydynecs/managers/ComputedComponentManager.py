"""pydynecs/manager/ComputedComponentManager.py
@OffbyOne Studios 2014
Computes existence of entity on the fly.
"""
import abc

from .. import abstract
from .. import core

class ComputedComponentManager(core.BaseManager, abstract.IReadableComponentManager):

    @abc.abstractmethod
    def compute(self, entity):
        pass
        
    def get(self, entity):
        return self.compute(entity)
        
    def has_entity(self, entity):
        if not self.dependencies_has_entity(entity):
            return False
        v = self.compute(entity)
        return not (v is None or v is False)
    
    def entities(self):
        return list(filter(self.has_entity, self.dependencies()[0][0].entities()))

    def values(self):
        return list(map(self.compute, self.dependencies()[0][0].entities()))
    
    def items(self):
        return list(map(lambda e: (e, self.compute(e)), self.entities()))
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __repr__(self):
        return "<IReadableComponentManager: {} entries>".format(len(self))