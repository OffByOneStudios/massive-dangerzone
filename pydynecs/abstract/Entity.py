"""pydynecs/abstract/Entity.py
@OffbyOne Studios 2014
Entity datatype.
"""

class Entity(object):
    def __init__(self, system, id, group=None):
        self.system = system
        self.id = id
        self.group = group
    
    def _get_key(self):
        return (self.system, self.id) if self.group is None else (self.system, self.id, self.group)
    
    def __hash__(self):
        return hash(self._get_key())
    
    def __eq__(self, other):
        return other == self._get_key()
    
    def __repr__(self):
        return "Entity{}".format(self._get_key())
