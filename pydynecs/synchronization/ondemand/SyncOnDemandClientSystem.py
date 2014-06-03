"""pydynecs/synchronization/ondemand/SyncOnDemandClientSystem.py
@OffbyOne Studios 2014
This provides on demand access to a remote ECS by pretending to be the system in question.
"""

from ... import abstract

class SyncOnDemandClientSystem(abstract.ISystem):
    def __init__(self, bind_str):
        pass
