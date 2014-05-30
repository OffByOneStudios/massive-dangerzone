"""pydynecs/manager/CheckedComponentManager.py
@OffbyOne Studios 2014
Does a user specified check on values before accepting them.
"""
import abc

from .. import abstract

class CheckError(Exception): pass

class CheckedComponentManager(abstract.IComponentManager):
    @abc.abstractmethod
    def check(self, value):
        pass

    def set(self, key, value):
        if not self.check(value):
            raise CheckedComponentManager.CheckError()
        super().set(key, value)
