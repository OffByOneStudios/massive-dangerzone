"""pyext/event.py
@OffbyOne Studios 2014
A library for creating events with syntactic suger.
"""

class UncallableEventHandler(Exception): pass

class Event(object):
    def __init__(self, name=None, sort=None):
        self._name = name
        self._calls = []
        self._sort = sort_key
    
    def __iadd__(self, other):
        if not callable(other):
            raise UncallableEventHandler("The event handler '{}' is not callable.".format(other))
        self._calls += other
        if not (self._sort is None):
            self._calls = self._sort(self._calls)
        return self
    
    def __isub__(self, other):
        if other in self._calls:
            self._calls.remove(other)
        return self
    
    def __call__(self, *args, **kwargs):
        for c in self._calls:
            c(*args, **kwargs)

