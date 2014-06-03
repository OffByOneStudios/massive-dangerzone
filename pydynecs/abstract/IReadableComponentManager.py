"""pydynecs/abstract/IReadableComponentManager.py
@OffbyOne Studios 2014
Abstract class used for retriving data related to entities.
"""
import abc

from . import *

class IReadableComponentManager(IEntityManager, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, entity):
        pass
    
    def has(self, entity):
        return self.has_entity(entity)
    
    @abc.abstractmethod
    def values(self):
        pass
    
    @abc.abstractmethod
    def items(self):
        pass
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __repr__(self):
        return "<IReadableComponentManager: {} entries>".format(len(self))
