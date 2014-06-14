"""madz/core/__init__.py
@OffbyOne Studios 2013
Module implementation features.
"""

from pydynecs import *

from .. import fileman


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

@manager
class Depends(CoercingComponentManager, BasicComponentManager, EntityClass):
    component_name="depends"
    def coerce(self, value): return list(value)

@manager
class Imports(CoercingComponentManager, BasicComponentManager, EntityClass):
    component_name="imports"
    def coerce(self, value): return list(value)

@manager
class Config(CheckedComponentManager, BasicComponentManager, EntityClass):
    component_name="Config"
    def check(self, value): return isinstance(value, config.Config)
