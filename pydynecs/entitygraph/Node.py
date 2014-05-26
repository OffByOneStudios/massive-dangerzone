from .. import abstract
from ..syntax import EntityFacade

class Node(abstract.IEntity):
    def __init__(self, nodetype, entity):
        self._nodetype = nodetype
        self._entity = entity
        self._entities = nodetype.expand(entity)

    def entity_id(self):
        return self._entity.entity_id()
    
    def __getitem__(self, key):
        return Node(self._entities[key])

    def __iter__(self):
        return self.

    def keys(self):
        return iter(self._entities)

    def __str__(self):
        return "<node: {} | {} list_keys, {} dict_keys>".format(self.entity_id(), list(self))
