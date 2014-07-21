"""pydynecs/synchronization/ondemand/SyncOnDemandEntityManager.py
@OffbyOne Studios 2014
This provides on demand access to an entity manager.
"""

from ... import abstract
from . import *

class SyncOnDemandEntityManager(abstract.IEntityManager, abstract.IManagerKey):
    @classmethod
    def meta(cls):
        return cls._net_meta
    
    @classmethod
    def pydynecs_key(self):
        return self._key
    
    def __init__(self, clientsys):
        self._clientsys = clientsys

    def get_system(self):
        return self._clientsys
    
    def dependencies(self):
        return []
    
    def has_entity(self, entity):
        return self._clientsys._query_has(self._key, entity)
        
    def entities(self):
        return self._clientsys._query_entities(self._key)
