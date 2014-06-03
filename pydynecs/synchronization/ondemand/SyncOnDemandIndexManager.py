"""pydynecs/synchronization/ondemand/SyncOnDemandIndexManager.py
@OffbyOne Studios 2014
This provides on demand access to a index manager.
"""

from ... import abstract
from . import *

class SyncOnDemandIndexManager(SyncOnDemandEntityManager, abstract.IIndexManager):
    def __init__(self, client, key):
        pass
