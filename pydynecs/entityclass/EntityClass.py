"""pydynecs/entityclass/EntityClass.py
@OffbyOne Studios 2014
Base class for constructing EntityClass implementations.
"""
import functools

from .. import abstract
from .. import core

def entity_property(func):
    func.__ecs_property__ = True
    return staticmethod(func)

class EntityClass(core.BaseManager, abstract.IEntityClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def expand_property(cls, property):
        property_actual = getattr(cls, property)
        return (property_actual,
            {
                "property_name": property
            })
    
    @classmethod
    def properties(cls):
        """A list of additional properties provided by this class, of the form:
        
        Each tuple is of the form:
        `(property, meta)`
        `property` is a provider for a property. A function that when called with an entity returns a descriptor (which may be assignable, and even deleatable). Where meta is a dictionary which may contain:
            * `property_name`: The name of the property.
        """
        return list(map(cls.expand_property, 
            filter(lambda p: hasattr(getattr(cls, p), "__ecs_property__"), 
                dir(cls))))
    
    def has_entity(self, entity):
        return self.dependencies_has_entity(entity)
    
    def entities(self):
        return list(filter(self.has_entity, self.dependencies()[0][0].entities()))