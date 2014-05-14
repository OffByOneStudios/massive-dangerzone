"""pyext/context.py
@OffbyOne Studios 2014
A library for provding multi methods.
"""
import functools

class MultiMethod(object):
    @staticmethod
    def _default_handler(*args, **kwargs):
        raise Exception("No default and no key found for: {}".format((args, kwargs)))
        
    def __init__(self, key_function):
        self._key = key_function
        self.default = MultiMethod._default_handler
        self._handlers = {}
    
    def key_for(self, *args, **kwargs):
        return self._key(*args, **kwargs)
    
    def register(self, key, func):
        self._handlers[key] = func
    
    def register_for(self, func, *args, **kwargs):
        self._handlers[self.key_for(*args, **kwargs)] = func
    
    def __call__(self, *args, **kwargs):
        key = self.key_for(*args, **kwargs)
        if key in self._handlers:
            return self._handlers[key](*args, **kwargs)
        else:
            return self.default(*args, **kwargs)

def multimethod(f):
    return functools.wraps(f)(MultiMethod(f))

def methodof(_multi, key):
    def _dec(f, multi=_multi):
        _multi.register(key, f)
        return f
    return _dec
