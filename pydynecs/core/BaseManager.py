"""pydynecs/core/BaseManager.py
@OffbyOne Studios 2014
Provides core features for managers.
"""
from pyext import *

from .. import abstract

class BaseManager(object):
    depends = []
    
    @classproperty
    def current(cls):
        return cls.pydynecs_ecsclass.current[cls]
    
    @classmethod
    def meta(cls):
        m = {}
        if hasattr(cls, "component_name") and issubclass(cls, abstract.IReadableComponentManager):
            m["component_name"] = cls.component_name
            
        manager_classification = ""
        if issubclass(cls, abstract.IIndexManager) and not (issubclass(cls, abstract.IReadableComponentManager)):
            manager_classification += "index"
        elif issubclass(cls, abstract.IReadableComponentManager) and not (issubclass(cls, abstract.IIndexManager)):
            manager_classification += "component"
        elif issubclass(cls, abstract.IReadableComponentManager) and issubclass(cls, abstract.IIndexManager):
            raise Exception("Bad classification, component and index")
        else:
            manager_classification = "entity"
            
        if issubclass(cls, abstract.IEntityClass):
            manager_classification += "-class"
        m["manager_classification"] = manager_classification
        
        return m
    
    def __init__(self, system):
        self._system = abstract.system(system)
        self._dependencies = list(map(lambda d: self.expand_dependency(d), self.get_dependencies()))
    
    def get_system(self):
        return self._system
    
    def get_dependencies(self):
        return self.depends
    
    def expand_dependency(self, depend):
        s = self.get_system()
        return (s[depend],
        {
            "key": depend
        })
    
    def dependencies(self):
        return list(self._dependencies)

    def dependencies_has_entity(self, entity):
        return all(list(map(lambda d: d[0].has_entity(entity), self.dependencies())))