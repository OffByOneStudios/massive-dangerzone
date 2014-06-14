"""pydynecs/relation/Relationship.py
@OffbyOne Studios 2013
Toplevel class for a relationship between two classes.
"""

import functools

class Relationship(object):
    pass

def relationship_component(prop):
    prop.__ecs_rel_component_property__ = True
    return prop