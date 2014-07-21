"""pydynecs/synchronization/ondemand/SyncOnDemandReadableComponentManager.py
@OffbyOne Studios 2014
This provides on demand access to a readable compoennt manager.
"""

from ... import abstract
from . import *

class SyncOnDemandReadableComponentManager(SyncOnDemandEntityManager, abstract.IReadableComponentManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get(self, entity):
        return self._clientsys._query_component(self, entity)
    
    def values(self):
        return [self._clientsys._query_component(self, entity) for entity in self.entities()]
        
    def items(self):
        return [(entity, self._clientsys._query_component(self, entity)) for entity in self.entities()]