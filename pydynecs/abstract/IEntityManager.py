"""pydynecs/abstract/IEntityManager.py
@OffbyOne Studios 2014
Abstract class used as a shared base managing collections of entities.

Specifically, provides features for dependencies between collections,
and managing basic features of collections in refrence to entities.
"""
import abc

class IEntityManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def dependencies(self):
        """Returns a list of tuples containg data on the collections this one
        depends on.
        
        Each tuple is of the form:
        `(collection, meta)`
        Collection is the concrete IEntityManager; where meta may contain:
            * key (the key this manager was found with)
        In addition to other data about how this manager uses the other.
        """
        pass
    
    @abc.abstractmethod
    def has_entity(self, entity):
        pass
    
    @abc.abstractmethod
    def entities(self):
        pass
    
    def __contains__(self, entity):
        return self.has_entity(entity)

    def __len__(self):
        return len(self.entities())
    
    def __iter__(self):
        return self.entities()
    
    def __repr__(self):
        return "<IEntityManager: {} entries>".format(len(self))
