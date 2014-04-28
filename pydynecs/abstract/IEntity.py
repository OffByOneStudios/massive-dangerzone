import abc

class IEntity(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def entity_id(self):
        """Returns the entity id."""
        pass
    
    def __hash__(self):
        return hash(self.entity_id())
    
    def __eq__(self, other):
        return isinstance(other, IEntity) and other.entity_id() == self.entity_id() 
    
    def __repr__(self):
        return "<IEntity: {}>".format(self.entity_id())
