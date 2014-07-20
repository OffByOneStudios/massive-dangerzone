"""pydynecs/synchronization/ondemand/SyncOnDemandReadableComponentManager.py
@OffbyOne Studios 2014
This provides on demand access to a readable compoennt manager.
"""

from ... import abstract
from . import *

class SyncOnDemandReadableComponentManager(SyncOnDemandEntityManager, abstract.IReadableComponentManager):
    def __init__(self, client, key):
        super().__init__(client, key)
        

    def get(self, entity):
        pass
    
    def values(self):
        return []
        
    def items(self):
        return []