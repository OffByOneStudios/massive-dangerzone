"""pyext/context.py
@OffbyOne Studios 2014
A library for provding multi-methods (incomplete).
"""

# TODO: Technique to resolve to the next function
# TODO: Better hierachy management

import abc
import collections
import functools
import inspect

class IMultiMethodStrategy(metaclass=abc.ABCMeta):
    """This is an abstract description of a multimethod implementation strategy.

    Instances of a strategy should be able to provide multiple stores and
    resolve bindings and calls against those stores.
    """

    @abc.abstractmethod
    def args_to_key(self, *args, **kwargs):
        """Takes live args (and kwargs) and generates a strategy specific key."""
        pass

    @abc.abstractmethod
    def binding_to_key(self, *args, **kwargs):
        """Takes binding args (and kwargs) and generates a strategy specific key."""
        pass

    @abc.abstractmethod
    def new_store(self):
        """Generate a store of bindings to resolve live objects against."""
        pass

    @abc.abstractmethod
    def add_entry(self, store, key, entry):
        """Using a key, add a callable resolution entry.

        Args:
            store: The store to store the entry in.
            key: The strategy specific key generated for the entry.
            entry: The callable to add.
        """
        pass

    @abc.abstractmethod
    def choose_entry(self, store, key, default):
        """Using a key, choose a callable resolution entry.

        Args:
            store: The store to find the entry in.
            key: The strategy specific key generated for the call.
            default: The defualt return value if a callable was not found.
        """
        pass

class MultiMethod(object):
    """Multimethod helper syntax, wraps a multimethod strategy to provide syntax.

    Attributes:
        default: The default function to call when the resolution strategy fails.
    """
    @staticmethod
    def _default_handler(*args, **kwargs):
        raise Exception("No default and no method found for: {}".format((args, kwargs)))

    def __init__(self, strategy):
        """Inits the multimethod using an IMultiMethodStrategy.

        Args:
            strategy: An instace of an IMultiMethodStrategy.

        Raises:
            Exception: if strategy is not an IMultiMethodStrategy.
        """

        if not isinstance(strategy, IMultiMethodStrategy):
            raise Exception("MultiMethod strategy must implement IMultiMethodStrategy")
        self._strategy = strategy
        self._store = strategy.new_store()
        self._handlers = {}
        self.default = MultiMethod._default_handler

    def key_for(self, *args, **kwargs):
        """Returns a strategy key for the given live args."""
        return self._strategy.args_to_key(*args, **kwargs)

    def key(self, *args, **kwargs):
        """Returns a strategy key for the given binding."""
        return self._strategy.binding_to_key(*args, **kwargs)

    def register(self, func, *args, **kwargs):
        """Registers a fundtion using the given binding.

        Args:
            func: The function to register.
            *args, **kwargs: The binding to register using.
        """
        self._strategy.add_entry(self._store, self._strategy.binding_to_key(*args, **kwargs), func)

    def register_for(self, func, *args, **kwargs):
        """Registers a fundtion using the given live args.

        Args:
            func: The function to register.
            *args, **kwargs: The live args to register using.
        """
        self._strategy.add_entry(self._store, self._strategy.args_to_key(*args, **kwargs), func)

    def function(self, *args, **kwargs):
        """Returns the function for the given binding."""
        return self._strategy.choose_entry(self._store, self._strategy.binding_to_key(*args, **kwargs), self.default)

    def would_call(self, *args, **kwargs):
        """Returns the function for the given live args."""
        return self._strategy.choose_entry(self._store, self._strategy.args_to_key(*args, **kwargs), self.default)

    def __call__(self, *args, **kwargs):
        """Calls a multimethod using the given live args."""
        return self._strategy.choose_entry(self._store, self._strategy.args_to_key(*args, **kwargs), self.default)(*args, **kwargs)

    def method(self, *args, **kwargs):
        """Returns a decorator which will add the decorated function using the given binding."""
        def dec(f, _self=self):
            _self.register(f, *args, **kwargs)
            return f
        return dec

def multimethod(o):
    """A decorator for creating MultiMethod instances using a strategy (instantiated or class)."""
    if inspect.isclass(o):
        o = o()
    return functools.wraps(o)(MultiMethod(o))



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
        if ArgMatchStrategy._sentinal in current:
            last_valid = current[ArgMatchStrategy._sentinal]
        return last_valid



class ClassResolutionStrategy(IMultiMethodStrategy):
    """The more common multimethod strategy, based of __mro__ of argument classes.

    Methods are bound by class arguments, the more specific classes are prefered.
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
