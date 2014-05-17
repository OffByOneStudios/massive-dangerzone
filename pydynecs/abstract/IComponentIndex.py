import abc

#TODO: May be able to be merged with readonly component managers
class IComponentIndex(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def attach(self, manager):
        """May only be called once."""
        pass
    
    @abc.abstractmethod
    def get(self, key):
        pass
    
    @abc.abstractmethod
    def has(self, key):
        pass
    
    @abc.abstractmethod
    def entities(self):
        pass
    
    @abc.abstractmethod
    def values(self):
        pass
    
    @abc.abstractmethod
    def items(self):
        pass
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __contains__(self, item):
        return self.has(item)

    def __len__(self):
        return len(self.entities())
    
    def __iter__(self):
        return self.entities()
    
    def __repr__(self):
        return "<IComponentIndex: {} entries>".format(len(self))
