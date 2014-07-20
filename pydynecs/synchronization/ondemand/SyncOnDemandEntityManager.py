"""pydynecs/synchronization/ondemand/SyncOnDemandEntityManager.py
@OffbyOne Studios 2014
This provides on demand access to an entity manager.
"""

from ... import abstract
from . import *

class SyncOnDemandEntityManager(abstract.IEntityManager):
    @classmethod
    def meta(cls):
        return cls._net_meta
    
    def __init__(self, clientsys, key):
        self._clientsys = clientsys
        self._key = key

    def get_system(self):
        return self._clientsys
    
    def dependencies(self):
        pass
    
    def has_entity(self, entity):
        pass
        
    def entities(self):
        pass
