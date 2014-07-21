"""pydynecs/synchronization/ondemand/SyncOnDemandIndexManager.py
@OffbyOne Studios 2014
This provides on demand access to a index manager.
"""

from ... import abstract
from . import *

class SyncOnDemandIndexManager(SyncOnDemandEntityManager, abstract.IIndexManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get(self, key):
        return self._clientsys._query_index(self, entity)
    
    def has(self, key):
        return not (self._clientsys._query_index(self, entity) is None)
    
    def keys(self):
        return []
    
    def items(self):
        return []
        