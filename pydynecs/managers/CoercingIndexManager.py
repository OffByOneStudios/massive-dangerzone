"""pydynecs/manager/CoercingIndexManager.py
@OffbyOne Studios 2014
Calls a function to mutate the value before setting it.
"""
import abc

from .. import abstract

class CoercingIndexManager(abstract.IIndexManager):
    @abc.abstractmethod
    def coerce(self, key):
        pass
    
    def get(self, key):
        k = self.coerce(key)
        return super().get(k)
    
    def has(self, key):
        k = self.coerce(key)
        return super().has(k)