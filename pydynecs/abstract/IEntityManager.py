"""pydynecs/abstract/IEntityManager.py
@OffbyOne Studios 2014
Abstract class used as a shared base managing collections of entities.

Specifically, provides features for dependencies between collections,
and managing basic features of collections in refrence to entities.
"""
import abc

class IEntityManager():
    @classmethod
    @abc.abstractmethod
    def meta(cls):
        """Returns a dictionary of metadata for this entity manager.
        
        * `component_name`: the name of this component
        """
        pass
    
    @abc.abstractmethod
    def get_system(self):
        pass
    
    @abc.abstractmethod
    def dependencies(self):
        """Returns a list of tuples containg data on the collections this one
        depends on.
        
        Each tuple is of the form:
        `(manager, meta)`
        `manager` is the concrete IEntityManager; where `meta` is a dictionary which may contain:
            * `key`: the key this manager was found with
        In addition to other data about how this manager uses the other.
        """
        pass
    
    @abc.abstractmethod
    def has_entity(self, entity):
        pass
    
    @abc.abstractmethod
    def entities(self):
        pass
    
    @property
    def s(self):
        return self.get_system()
    
    def __contains__(self, entity):
        return self.has_entity(entity)

    def __len__(self):
        return len(self.entities())
    
    def __iter__(self):
        return self.entities()
    
    def __repr__(self):
        return "<IEntityManager: {} entries>".format(len(self))
