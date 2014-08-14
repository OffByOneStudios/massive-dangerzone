"""pyext/latebind.py
@OffbyOne Studios 2014
Provides a latebinding descriptor. Which warns on multiple assign, and excepts or performs functionality on non-assignment.
"""

import warnings
import functools

class LateBindingDescriptor(object):
    """A desciptor for variables which will be bound on first access, or set at a later time."""
    def __init__(self, _latebind=None, _nowarn=False):
        """Creates a latebinding.

        Args:
            _latebind: optional function to create the latebinding on demand.
            _nowarn: if true disable warnings on multple binding (default false).
        """

        if not (_latebind is None):
            self._latebind = _latebind
        self._cache = None
        self._nowarn = _nowarn

    def _latebind(self):
        """Default latebind binding, can be overriden as an object attribute."""
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
    """Decorator for wrapping `LateBindingDescriptor`s, the function becomes the latebind function getter."""
    return functools.wraps(func)(LateBindingDescriptor(func))

