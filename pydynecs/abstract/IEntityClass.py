"""pydynecs/abstract/IEntityClass.py
@OffbyOne Studios 2014
Describes classes of entites, represented by membership in a number of entity managers, hence it is also an entity manager.

Provides additional functionality for classes of entities, and facilitates the creation of facades towards that goal.
"""
import abc

from .IEntityManager import IEntityManager

class IEntityClass(IEntityManager, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def properties(self):
        """A list of additional properties provided by this class, of the form:
        
        Each tuple is of the form:
        `(property, meta)`
        `property` is a provider for a property. A function that when called with an entity returns a descriptor (which may be assignable, and even deleatable). Where meta is a dictionary which may contain:
            * `property_name`: The name of the property.
        """
        pass
