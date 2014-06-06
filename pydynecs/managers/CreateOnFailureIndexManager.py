"""pydynecs/manager/CreateOnFailureIndexManager.py
@OffbyOne Studios 2014
Creates new entities on failure
"""
import abc

from .. import abstract

class CreateOnFailureIndexManager(abstract.IIndexManager):
    @abc.abstractmethod
    def create(self, key):
        pass
    
    def get(self, key):
        try:
            return super().get(key)
        except:
            return self.create(key)
    
    def has_entity(self, entity):
        return self.dependencies_has_entity(entity)