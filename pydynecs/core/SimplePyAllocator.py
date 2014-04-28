from .. import abstract

abstract.IEntity.register(tuple)
abstract.IEntity.register(int)

class SimplePyAllocator(abstract.IEntityAllocator):
    class SimpleEntity(abstract.IEntity):
        def __init__(self, tup):
            self._v = tup
        def entity_id(self):
            return self._v

    def __init__(self):
        self._last_entity = 0
        self._last_hinted = 0
        self._hints = {}
        self._hints_last_entity = {}
        
        self._save_last = None
        
        self._reclaimed = []
    
    def new_entity(self, hint=None):
        if hint is None:
            self._last_entity += 1
            self._save_last = self._last_entity
            return SimplePyAllocator.SimpleEntity(self._save_last)
        
        if not (hint in self._hints):
            self._last_hinted += 1
            self._hints[hint] = self._last_hinted
            self._hints_last_entity[self._last_hinted] = 0
        
        hinter = self._hints[hint]
        self._hints_last_entity[hinter] += 1
        self._save_last = (hinter, self._hints_last_entity[hinter])
        return SimplePyAllocator.SimpleEntity(self._save_last)
    
    def last_entity(self):
        return SimplePyAllocator.SimpleEntity(self._save_last)

    def valid_entity(self, entity):
        if isinstance(entity, abstract.IEntity):
            tup = entity.entity_id()
        else:
            return False
        
        if isinstance(tup, int) and tup <= self._last_entity:
            return True
        elif (isinstance(tup, tuple)
            and len(tup) == 2
            and tup[0] <= self._last_hinted
            and tup[1] <= self._hints_last_entity[tup[0]]):
            return True
        else:
            return False
    
    def reclaim_entity(self, entity):
        self._reclaimed.append(entity)
    
