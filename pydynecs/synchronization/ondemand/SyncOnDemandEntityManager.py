"""pydynecs/synchronization/ondemand/SyncOnDemandEntityManager.py
@OffbyOne Studios 2014
This provides on demand access to an entity manager.
"""

from ... import abstract
from . import *

class SyncOnDemandEntityManager(abstract.IEntityManager):
    def __init__(self, client, key):
        pass
