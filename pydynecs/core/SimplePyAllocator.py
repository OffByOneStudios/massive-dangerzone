from .. import abstract

class SimplePyAllocator(abstract.IEntityAllocator):
    def __init__(self, system):
        self._last_entity = 0
        self._last_hinted = 0
        self._hints_last_entity = {}
        
        self._save_last = None
        
        self._reclaimed = []
        self._system = abstract.system(system)
    
    def new_entity(self, hint=None):
        if not (hint in self._hints_last_entity):
            self._hints_last_entity[hint] = 0
        
        self._hints_last_entity[hint] += 1
        self._save_last = abstract.Entity(self._system, self._hints_last_entity[hint], hint)
        return self._save_last
    
    def last_entity(self):
        return self._save_last

    def valid_entity(self, potential_e):
        ent = abstract.entity(potential_e)
        
        return (isinstance(ent, abstract.Entity)
            and ent.system == self._system
            and ent.id <= self._hints_last_entity[ent.group])
    
    def reclaim_entity(self, entity):
        self._reclaimed.append(entity)
    
