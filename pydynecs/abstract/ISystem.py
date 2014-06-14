"""pydynecs/abstract/ISystem.py
@OffbyOne Studios 2014
Description of classes which represent systems of managers and entities.
"""
import abc

from .IEntityAllocator import *

class ISystem(IEntityAllocator, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_manager(self, key):
        pass
    
    @classmethod
    @abc.abstractmethod
    def add_manager(self, key, manager_class):
        pass
    
    @abc.abstractmethod
    def managers(self):
        """Returns key-value-pairs of (key, IComponentManager instance)."""
        pass
    
    def __getitem__(self, key):
        return self.get_manager(key)

    def __repr__(self):
        return "<ISystem: {} managers>".format(len(self.managers()))
    
    def managers_of(self, entity):
        return [(key, m) for key, m in self.managers() if m.has_entity(entity)]
    
    def components_of(self, entity):
        return {key: m.get(entity) for key, m in self.managers_of(entity)}
