"""bootstrap/folder_loader.py
@OffbyOneStudios 2013
Core features of bootstrapped plugin system
"""

from pydynecs import *

## Ecs System
@system_syntax
class EcsBootstrap(System): pass
EcsBootstrap.current = EcsBootstrap()
manager = manager_decorator_for(EcsBootstrap)

## Core Components

@manager
class Name(ObservableComponentManager, CoercingComponentManager, BasicComponentManager):
    coerce = str

@manager
class Name_lookup(LookupIndexManager):
    source = Name
    def key(self, plugin):
        return self.s[Name][plugin]

@manager
class PyModule(ObservableComponentManager, CoercingComponentManager, BasicComponentManager):
    coerce = str

@manager
class PyModule_lookup(LookupIndexManager):
    source = PyModule
    def key(self, plugin):
        return self.s[PyModule][plugin]
        
@manager
class Object(BasicComponentManager): pass

@manager
class Dependencies(CoercingComponentManager, BasicComponentManager):
    coerce = list

class BootstrapPluginImplementationComponentManager(CheckedComponentManager, BasicComponentManager):
    interface = type
    def check(self, value):
        return issubclass(value, self.interface)
    
    def instances(self, *args, **kwargs):
        for implementation in self.values():
            #TODO(Mason): Some way of dealing with erros in construction?
            yield implementation(*args, **kwargs)

def add_bootstrap_plugin(name, plugin):
    sys = EcsBootstrap.current
    e = Entity()
    e[Name] = name
    e[PyModule] = plugin.__module__
    e[Object] = plugin
    
    for _, manager in sys.managers():
        if isinstance(manager, CheckedComponentManager) and manager.check(plugin):
            manager[e] = plugin
    return plugin

def bootstrap_plugin(name):
    return lambda p, n=name: add_bootstrap_plugin(n, p)

def bootstrap_ensure_module(name):
    if not name in EcsBootstrap.current[Name_lookup]:
        #try:
        import importlib
        importlib.import_module(name)
        return EcsBootstrap.current[Name_lookup][name]
        #except:
        #    pass
    else:
        return EcsBootstrap.current[Name_lookup][name]
