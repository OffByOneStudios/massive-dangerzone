"""pydynecs/core/BaseManager.py
@OffbyOne Studios 2014
Provides core features for managers.
"""

from .. import abstract

class BaseManager(object):
    depends = []
    
    def __init__(self, system):
        self._system = abstract.system(system)
        self._dependencies = list(map(lambda d: self.expand_dependency(d), self.get_dependencies()))
    
    def meta(self):
        m = {}
        if hasattr(self, "component_name") and isinstance(self, abstract.IReadableComponentManager):
            m["component_name"] = self.component_name
        return m
    
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