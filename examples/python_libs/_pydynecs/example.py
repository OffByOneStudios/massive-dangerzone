"""examples/python_libs/_pydynecs/example.py
@OffbyOne Studios 2014
An example entity component system. This will create the classes and load the data for other testing.

The ECS system will have the name Widget, entities will represent Widgets of some sort.
"""

import pydynecs as ecs

class WidgetSystem(ecs.System): pass
ecs.inject_syntax_for(__name__, WidgetSystem)
