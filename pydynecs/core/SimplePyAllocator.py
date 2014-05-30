from .. import abstract

class SimplePyAllocator(abstract.IEntityAllocator):
    def __init__(self, prefix):
        self._last_entity = 0
        self._last_hinted = 0
        self._hints = {}
        self._hints_last_entity = {}
        
        self._save_last = None
        
        self._reclaimed = []
        self._prefix = prefix
    
    def new_entity(self, hint=None):
        if not (hint in self._hints):
            self._last_hinted += 1
            self._hints[hint] = self._last_hinted
            self._hints_last_entity[self._last_hinted] = 0
        
        hinter = self._hints[hint]
        self._hints_last_entity[hinter] += 1
        self._save_last = (self._prefix, hinter, self._hints_last_entity[hinter])
        return self._save_last
    
    def last_entity(self):
        return self._save_last

    def valid_entity(self, potential_e):
        tup = abstract.entity(potential_e)
        
        if (isinstance(tup, tuple)
            and (len(tup) == 3
                and tup[0] == self._prefix 
                and tup[1] <= self._last_hinted
                and tup[2] <= self._hints_last_entity[tup[1]])):
            return True
        else:
            return False
    
    def reclaim_entity(self, entity):
        self._reclaimed.append(entity)
    
