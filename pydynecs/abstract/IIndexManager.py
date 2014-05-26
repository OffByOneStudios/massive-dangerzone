"""pydynecs/abstract/IIndexManager.py
@OffbyOne Studios 2014
Abstract class used for describing indexs of entities.
"""
import abc

from . import *

class IIndexManager(IEntityManager, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def get(self, key):
        """Get entity by key."""
        pass
    
    @abc.abstractmethod
    def has(self, key):
        """Has key."""
        pass
    
    @abc.abstractmethod
    def keys(self):
        """Iterable of keys."""
        pass
    
    @abc.abstractmethod
    def items(self):
        """Iterable of (key, value) tuples."""
        pass
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __contains__(self, item):
        return self.has(item)
    
    def __repr__(self):
        return "<IIndexManager: {} entries>".format(len(self))
