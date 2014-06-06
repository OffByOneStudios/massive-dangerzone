"""pyext/latebind.py
@OffbyOne Studios 2014
Provides a latebinding descriptor. Which warns on multiple assign, and excepts or performs functionality on non-assignment.
"""

import warnings
import functools

class LateBindingDescriptor(object):
    def __init__(self, _latebind=None, _nowarn=False):
        if not (_latebind is None):
            self._latebind = _latebind
        self._cache = None
        self._nowarn = _nowarn
    
    def _latebind(self):
        raise Exception("Latebinding for {} not set.".format(self.__qualname__))
    
    def __get__(self, obj, type):
        if self._cache is None:
            res = self._latebind()
            if not (res is None):
                self._cache = res
        return self._cache
    
    def __set__(self, obj, value):
        if not (self._cache is None or self._nowarn):
            warnings.warn("Latebinding for {} already set.".format(self.__qualname__))
        self._cache = value

def latebind(func):
    return functools.wraps(func)(LateBindingDescriptor(func))

