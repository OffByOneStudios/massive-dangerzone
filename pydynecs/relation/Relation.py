"""pydynecs/relation/Relation.py
@OffbyOne Studios 2013
Toplevel class for a relationship between two classes.
"""

from .RelationManager import *
from .Relationship import *

class RelationMeta(object):
    def __init__(self, name, bases, attrs):
        # Collect relationship manager classes
        
        # Calculate systems

class Relation(metaclass=RelationMeta):
    def __init__(self, systems):
        self._system = set(systems)
        self._manager_lookup = {}
        for rmanager in self._relation_managers:
            self._manager_lookup[sys] = rmanager