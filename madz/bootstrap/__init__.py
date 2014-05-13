"""bootstrap/__init__.py
@OffbyOneStudios 2013
A bootstrapped plugin system for madz
"""

import pydynecs

class BootstrapPluginSystem(pydynecs.System): pass
BootstrapPluginSystem.current = BootstrapPluginSystem()
pydynecs.inject_syntax_for(__name__, BootstrapPluginSystem)

pydynecs.inject_syntax_manager(__name__, BootstrapPluginSystem.current,
                          "Name", pydynecs.CoercingComponentManager(str))
pydynecs.inject_syntax_manager(__name__, BootstrapPluginSystem.current,
                          "Dependencies", pydynecs.CoercingComponentManager(list))

class BootstrapPluginImplementationComponentManager(pydynecs.CheckedComponentManager):
    def __init__(self, interface=type):
        super().__init__(lambda t, inter=interface: issubclass(t, inter))
        self.interface = interface
    
    def instances(self, *args, **kwargs):
        for implementation in self.values():
            #TODO(Mason): Some way of dealing with erros in construction?
            yield implementation(*args, **kwargs)

class BootstrapPluginInstanceComponentManager(pydynecs.CheckedComponentManager):
    def __init__(self, interface=object):
        super().__init__(lambda t, inter=interface: isinstance(t, inter))
        self.interface = interface

def add_bootstrap_plugin(name, plugin):
    sys = BootstrapPluginSystem.current
    e = Entity()
    e[Name] = name
    
    for manager in sys.managers():
        if isinstance(manager, BootstrapPluginImplementationComponentManager) \
          and issubclass(plugin, manager.interface):
            manager[e] = plugin
        if isinstance(manager, BootstrapPluginInstanceComponentManager) \
          and isinstance(plugin, manager.interface):
            manager[e] = plugin

def bootstrap_plugin(name):
    return lambda p, n=name: bootstrap_plugin(n, p)