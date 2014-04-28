import abc

class IComponentManager(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def get(self, key):
        pass
    
    @abc.abstractmethod
    def set(self, key, value):
        pass
    
    @abc.abstractmethod
    def des(self, key):
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
    
    def __setitem__(self, key, item):
        return self.get(key, item)
    
    def __delitem__(self, key):
        return self.des(key)
    
    def __contains__(self, item):
        return self.has(key)

    def __len__(self):
        return len(self.entities())
    
    def __iter__(self):
        return self.entities()
    
    def __repr__(self):
        return "<IComponentManager: {} entries>".format(len(self.entities()))
