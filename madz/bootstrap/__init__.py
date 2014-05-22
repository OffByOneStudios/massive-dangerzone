"""bootstrap/__init__.py
@OffbyOneStudios 2013
A bootstrapped plugin system for madz
"""
from pydynecs import *

class EcsBootstrapSystem(System): pass
EcsBootstrap = EcsBootstrapSystem()
syntax_for(EcsBootstrap)

manager = manager_for(EcsBootstrap)
index = lambda m: index_for(EcsBootstrap, m)

@manager
class Name(CoercingComponentManager):
    coerce = str

@manager
class Object(BasicComponentManager): pass

@manager
class Dependencies(CoercingComponentManager):
    coerce = list

class BootstrapPluginImplementationComponentManager(CheckedComponentManager):
    interface = type
    def check(self, value):
        return issubclass(value, self.interface)
    
    def instances(self, *args, **kwargs):
        for implementation in self.values():
            #TODO(Mason): Some way of dealing with erros in construction?
            yield implementation(*args, **kwargs)

class BootstrapPluginInstanceComponentManager(CheckedComponentManager):
    interface = type
    def check(self, value):
        return isinstance(value, self.interface)

def add_bootstrap_plugin(name, plugin):
    sys = EcsBootstrap.current
    e = Entity()
    e[Name] = name
    e[Object] = plugin
    
    for _, manager in sys.managers():
        if isinstance(manager, CheckedComponentManager) and manager.check(plugin):
            manager[e] = plugin
    return plugin

def bootstrap_plugin(name):
    return lambda p, n=name: add_bootstrap_plugin(n, p)
