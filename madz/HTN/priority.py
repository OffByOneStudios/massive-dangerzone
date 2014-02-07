from abc import *

def priority_to_key(priority):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return priority.compare(self.obj, other.obj) < 0
        def __gt__(self, other):
            return priority.compare(self.obj, other.obj) > 0
        def __eq__(self, other):
            return priority.compare(self.obj, other.obj) == 0
        def __le__(self, other):
            return priority.compare(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return priority.compare(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return priority.compare(self.obj, other.obj) != 0
    return K

class IPriority(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare(self, a, b):
        pass

class PriorityShortCircut(IPriority):
    def __init__(self, priorities):
        self._priorities = priorities

    def compare(self, a, b):
        for priority in self._priorities:
            r = priority.compare(a, b)
            if r != 0:
                return r
        return 0

class PriortityRank(IPriority):
    def __init__(self, ranks, default=0):
        self._ranks = dict(ranks)
        self._default = default

    def compare(self, a, b):
        rank_a = self._ranks.get(a, self._default)
        rank_b = self._ranks.get(b, self._default)

        return rank_b - rank_a
