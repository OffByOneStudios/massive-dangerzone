"""madz/core/__init__.py
@OffbyOne Studios 2013
Module implementation features.
"""

from pydynecs import *

from .. import fileman
from ..config import BaseConfig

from .plugin_id import *

@system_syntax
class EcsModules(System): pass
EcsModules.current = EcsModules()
manager = manager_decorator_for(EcsModules)

@manager
class Id(ObservableComponentManager, CoercingComponentManager, BasicComponentManager):
    component_name="id"
    def coerce(self, value): return PluginId.coerce(value, complete=True)
    
@manager
class Id_lookup(CoercingIndexManager, LookupIndexManager):
    source=Id
    def coerce(self, key): return PluginId.coerce(value, complete=False)

    def key(self, entity):
        return self.s[Id][entity]

class ModuleModuleRelationship(object):
    def __init__(self, source=None, target=None):
        self.source = entity(source)
        self.target = entity(target)
    
    def build(self):
        module_relation = EcsModules.current[Modules]
        if not (self.source in module_relation):
            module_relation[self.source] = ({}, {})
        if not (self.target in module_relation):
            module_relation[self.target] = ({}, {})
        module_relation[self.source][0][self.target] = self
        module_relation[self.target][1][self.source] = self

class RequiresRelationship(ModuleModuleRelationship): pass
class DependsRelationship(RequiresRelationship): pass
class ImportsRelationship(RequiresRelationship): pass

@manager
class Modules(CheckedComponentManager, BasicComponentManager, EntityClass):
    component_name="modules"
    def check(self, value): return EcsModules.current.valid_entity(value)
    
    @entity_property
    def source_of_relations(s, e, relation_class):
        (sourced, targeted) = s[Modules][e]
        return list(filter(lambda r: isinstance(r, relation_class), sourced.values()))

    @entity_property
    def target_of_relations(s, e, relation_class):
        (sourced, targeted) = s[Modules][e]
        return list(filter(lambda r: isinstance(r, relation_class), targeted.values()))

@manager
class Config(CheckedComponentManager, BasicComponentManager, EntityClass):
    component_name="config"
    def check(self, value): return isinstance(value, BaseConfig)
