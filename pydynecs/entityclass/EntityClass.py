"""pydynecs/entityclass/EntityClass.py
@OffbyOne Studios 2014
Base class for constructing EntityClass implementations.
"""

from .. import abstract

class EntityClass(abstract.IEntityClass):
    @classmethod
    def construct(cls, **kwargs):
        pass
    
    @classmethod
    def inflate(cls, entity):
        return cls(entity)
    
    def __init__(self, entity):
        pass