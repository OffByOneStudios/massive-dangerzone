"""pydynecs/abstract/IComponentManager.py
@OffbyOne Studios 2014
Abstract class used for managing data related to entities.
"""
import abc

from . import *

class IComponentManager(IReadableComponentManager):
    @abc.abstractmethod
    def set(self, entity, value):
        pass
    
    @abc.abstractmethod
    def des(self, entity):
        pass
    
    def __setitem__(self, key, item):
        return self.set(key, item)
    
    def __delitem__(self, key):
        return self.des(key)
    
    def __repr__(self):
        return "<IComponentManager: {} entries>".format(len(self))
