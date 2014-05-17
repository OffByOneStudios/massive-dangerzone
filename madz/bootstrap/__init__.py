"""bootstrap/__init__.py
@OffbyOneStudios 2013
A bootstrapped plugin system for madz
"""
from pydynecs import *

class EcsBootstrapSystem(System): pass
EcsBootstrap = EcsBootstrapSystem()
syntax_for(EcsBootstrap)

syntax_manager(
    EcsBootstrap,
    "Name",
    CoercingComponentManager(str))
syntax_manager(
    EcsBootstrap,
    "Object",
    BasicComponentManager())
syntax_manager(
    EcsBootstrap,
    "Dependencies",
    CoercingComponentManager(list))

class BootstrapPluginImplementationComponentManager(CheckedComponentManager):
    def __init__(self, interface=type):
        super().__init__(lambda t, inter=interface: issubclass(t, inter))
        self.interface = interface
    
    def instances(self, *args, **kwargs):
        for implementation in self.values():
            #TODO(Mason): Some way of dealing with erros in construction?
            yield implementation(*args, **kwargs)

class BootstrapPluginInstanceComponentManager(CheckedComponentManager):
    def __init__(self, interface=object):
        super().__init__(lambda t, inter=interface: isinstance(t, inter))
        self.interface = interface

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