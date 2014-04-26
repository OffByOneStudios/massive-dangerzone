"""pyext/context.py
@OffbyOne Studios 2014
A library for managing context variables, specifically across threads.

Includes helpers for singletons.
"""

import threading
import contextlib

_contexts = {}

class ExistingContextVariableError(Exception): pass
class MissingContextVariableError(Exception): pass

def collect_context():
    """Collect the entire current context and save it to a dictionary."""
    global _contexts
    return {key: var.get() for (key, var) in _contexts.items()}

def expand_context(context, safe=True):
    """Expand a context dictionary into the current context."""
    global _contexts
    for key, value in context.items():
        get_variable(key, safe=safe).set(value)

@contextlib.contextmanager
def the_context(context):
    """With a context dictionary as the current context."""
    old_context = collect_context()
    try:
        expand_context(context)
        yield
    finally:
        expand_context(old_context)

def get_variable(key, safe=False):
    """Get a context variable by key."""
    global _contexts
    if key in _contexts:
        return _contexts[key]
    elif safe:
        return ContextVariable(key)
    else:
        raise MissingContextVariableError("The context variable '{}' is missing.".format(key))

class ContextVariable(object):
    """An object representing a context variable."""
    
    def __init__(self, key, glb=None):
        """Construct a new variable. Should be done at the global or class scope.
        
        Args:
            key: The class, or a global key of some sort, for this variable.
            glb: The global default value of this variable.
        """
        global _contexts
        
        if (key in _contexts):
            raise ExistingContextVariableError("The context variable '{}' is already in use.".format(key))
        
        # Set thread local object before adding to context dictionary for thread safety.
        self._local = threading.local()
        self._local.value = glb
        
        _contexts[key] = self
        self._key = key
    
    def destroy(self):
        del _contexts[self._key]
        self._local = None
    
    def get(self):
        """Get variable value."""
        return self._local.value
    
    def set(self, value):
        """Set variable value."""
        self._local.value = value
        return self.get()
    
    @contextlib.contextmanager
    def set_to(self, value):
        """With the variable value."""
        old_value = self.get()
        try:
            yield self.set(value)
        finally:
            self.set(old_value)
    
    def __str__(self):
        return "{}({}): {}".format(self.__class__.__name__, self._key, self.get())
    
    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self._key, self.get())

        