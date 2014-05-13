"""bootstrap/__init__.py
@OffbyOneStudios 2013
A bootstrapped plugin system for madz
"""

import pydynecs as ecs

class BootstrapPluginSystem(ecs.System): pass
BootstrapPluginSystem.current = BootstrapPluginSystem()
ecs.inject_syntax_for(__name__, BootstrapPluginSystem)

ecs.inject_syntax_manager(__name__, BootstrapPluginSystem.current,
                          "Name", ecs.CoercingComponentManager(str))
ecs.inject_syntax_manager(__name__, BootstrapPluginSystem.current,
                          "Dependencies", ecs.CoercingComponentManager(list))
