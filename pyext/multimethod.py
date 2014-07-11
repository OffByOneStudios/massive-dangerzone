"""pyext/context.py
@OffbyOne Studios 2014
A library for provding multi methods.
"""
# TODO: resolve to next function

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

class ClassResolutionStrategy(IMultiMethodStrategy):
    """The common multimethod strategy, based of mro of arguments.
    
    Methods are bound by class arguments, the more specific classes are preffered.
    """
    def __init__(self, onclass=False):
        """If onclass is true, assumes this is on a class and method calls will be invoked."""
        self._methods = onclass
        
    def args_to_key(self, *args, **kwargs):
        if self._methods:
            args = args[1:]
        return tuple(map(type, args))
    
    def binding_to_key(self, *args, **kwargs):
        return tuple(args)
    
    class Store(object):
        class _sentinal: pass
        class _lookup_failure: pass
        
        def __init__(self):
            self._cache = {}
            self._lookup = {}
        
        def add(self, bind, value):
            self._cache = {}
            current = self._lookup
            for t in bind:
                if not (t in current):
                    current[t] = {}
                current = current[t]
            current[ClassResolutionStrategy.Store._sentinal] = value
        
        @staticmethod
        def _lookup(current, key):
            if not key:
                return current[ClassResolutionStrategy.Store._sentinal]
            
            for mro in key[0].__mro__:
                if not (mro in current):
                    continue
                    
                v = ClassResolutionStrategy.Store._lookup(current[mro], key[1:])
                
                if v is ClassResolutionStrategy.Store._lookup_failure:
                    continue
                
                return v
            
            return ClassResolutionStrategy.Store._lookup_failure
        
        def lookup(self, key):
            if key in self._cache:
                return self._cache[key]
            else:
                v = ClassResolutionStrategy.Store._lookup(self._lookup, key)
                self._cache[key] = v
                return v
    
    def new_store(self):
        return self.Store()
    
    def add_entry(self, store, key, entry):
        store.add(key, entry)
    
    def choose_entry(self, store, key, default):
        v = store.lookup(key)
        if v is ClassResolutionStrategy.Store._lookup_failure:
            return default
        return v
