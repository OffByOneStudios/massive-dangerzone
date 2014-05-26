"""pydynecs/abstract/IComponentManager.py
@OffbyOne Studios 2014
Abstract class used for managing data related to entities.
"""
import abc

from . import *

class IComponentManager(IEntityManager, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, entity):
        pass
    
    @abc.abstractmethod
    def set(self, entity, value):
        pass
    
    @abc.abstractmethod
    def des(self, entity):
        pass
    
    def has(self, entity):
        return has_entity(entity)
    
    @abc.abstractmethod
    def values(self):
        pass
    
    @abc.abstractmethod
    def items(self):
        pass
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, item):
        return self.set(key, item)
    
    def __delitem__(self, key):
        return self.des(key)
    
    def __repr__(self):
        return "<IComponentManager: {} entries>".format(len(self))
