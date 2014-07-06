"""pyext/context.py
@OffbyOne Studios 2014
A library for provding multi methods.
"""
import abc
import collections
import functools
import inspect

class IMultiMethodStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def args_to_key(self, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    def binding_to_key(self, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    def new_store(self):
        pass
        
    @abc.abstractmethod
    def add_entry(self, store, key, entry):
        pass
    
    @abc.abstractmethod
    def choose_entry(self, store, key, default):
        pass

class MultiMethod(object):
    @staticmethod
    def _default_handler(*args, **kwargs):
        raise Exception("No default and no method found for: {}".format((args, kwargs)))
        
    def __init__(self, strategy):
        if not isinstance(strategy, IMultiMethodStrategy):
            raise Exception("MultiMethod strategy must implement IMultiMethodStrategy")
        self._strategy = strategy
        self._store = strategy.new_store()
        self.default = MultiMethod._default_handler
        self._handlers = {}
    
    def key_for(self, *args, **kwargs):
        return self._strategy.args_to_key(*args, **kwargs)
    
    def key(self, *args, **kwargs):
        return self._strategy.binding_to_key(*args, **kwargs)
    
    def register(self, func, *args, **kwargs):
        self._strategy.add_entry(self._store, self._strategy.binding_to_key(*args, **kwargs), func)
    
    def register_for(self, func, *args, **kwargs):
        self._strategy.add_entry(self._store, self._strategy.args_to_key(*args, **kwargs), func)
    
    def function(self, *args, **kwargs):
        return self._strategy.choose_entry(self._store, self._strategy.binding_to_key(*args, **kwargs), self.default)
    
    def would_call(self, *args, **kwargs):
        return self._strategy.choose_entry(self._store, self._strategy.args_to_key(*args, **kwargs), self.default)
    
    def __call__(self, *args, **kwargs):
        return self._strategy.choose_entry(self._store, self._strategy.args_to_key(*args, **kwargs), self.default)(*args, **kwargs)

def multimethod(o):
    if inspect.isclass(o):
        o = o()
    return functools.wraps(o)(MultiMethod(o))

def methodof(_multi, *args, **kwargs):
    def _dec(f, multi=_multi):
        _multi.register(f, *args, **kwargs)
        return f
    return _dec

class ArgMatchStrategy(IMultiMethodStrategy):
    """A very simple matching multimethod strategy
    
    Methods are called only if the method is bound to the least subset of the
    arguments, ignoring keyword arguments.
    """
    def __init__(self, onclass=False):
        """If onclass is true, assumes this is on a class and method calls will be invoked."""
        self._methods = onclass
        
    class _sentinal: pass
    
    def args_to_key(self, *args, **kwargs):
        if self._methods:
            args = args[1:]
        return (args, kwargs)
    
    def binding_to_key(self, *args, **kwargs):
        return (args, kwargs)
    
    def new_store(self):
        return dict()
    
    def add_entry(self, store, key, entry):
        args, kwargs = key
        
        current = store
        for arg in args:
            if not (arg in current):
                current[arg] = dict()
            current = current[arg]
        current[ArgMatchStrategy._sentinal] = entry
    
    def choose_entry(self, store, key, default):
        args, kwargs = key
        
        kwset = set(kwargs)
        
        last_valid = default
        current = store
        for arg in args:
            if ArgMatchStrategy._sentinal in current:
                last_valid = current[ArgMatchStrategy._sentinal]
            if isinstance(arg, collections.Hashable) and arg in current:
                current = current[arg]
            else:
                break;
        
        return last_valid
