"""pydynecs/manager/CoercingComponentManager.py
@OffbyOne Studios 2014
Calls a function to mutate the value before setting it.
"""
import abc

from .. import abstract

class CoercingComponentManager(abstract.IComponentManager):
    @abc.abstractmethod
    def coerce(self, value):
        pass
    
    def set(self, key, value):
        v = self.coerce(value)
        super().set(key, v)
