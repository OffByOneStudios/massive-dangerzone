import abc

from .IEntityAllocator import *

class ISystem(IEntityAllocator, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_manager(self, key):
        pass
    
    @abc.abstractmethod
    def add_manager(self, key, manager):
        pass
    
    @abc.abstractmethod
    def managers(self):
        """Returns key-value-pairs of (key, IComponentManager instance)."""
        pass
    
    @abc.abstractmethod
    def get_index(self, key):
        pass
    
    @abc.abstractmethod
    def add_index(self, key, index):
        pass
    
    @abc.abstractmethod
    def indicies(self):
        """Returns key-value-pairs of (key, IComponentIndex instance)."""
        pass
    
    def __getitem__(self, key):
        try:
            return self.get_manager(key)
        except KeyError:
            pass
        return self.get_index(key)

    def __repr__(self):
        return "<ISystem: {} managers, {} indicies>".format(len(self.managers()), len(self.indicies()))
    
    def managers_of(self, entity):
        return [(key, m) for key, m in self.managers() if m.has(entity)]
    
    def components_of(self, entity):
        return {key: m.get(entity) for key, m in self.managers_of(entity)}
