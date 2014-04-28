import abc

class IEntityAllocator(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def new_entity(self, hint=None):
        """Creates a new id, hint is a unique key for a class of entities. For now. Eventually it will need to provide allocation help."""
        pass
    
    @abc.abstractmethod
    def last_entity(self):
        """The last entity we returned."""
        pass

    @abc.abstractmethod
    def valid_entity(self, entity):
        """Test if an entity is valid for this allocator."""
        pass
    
    @abc.abstractmethod
    def reclaim_entity(self, entity):
        """Called when every component of an entity has been deleted."""
        pass
    
