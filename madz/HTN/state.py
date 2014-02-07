from abc import *

###
### Abstract Bases
###

class IState(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def copy(self):
        """Copies this state object."""
        pass

    @classmethod
    @abstractmethod
    def key(cls):
        """Gets the key of this state object."""
        pass

###
### StateCollection
###

class StateCollection(object):
    def __init__(self, state_objects):
        self._ensureStateObjects(state_objects)
        self._states = {s.key(): s.copy() for s in state_objects}

    def __getitem__(self, state):
        return self._states[state.key()]

    def _ensureStateObjects(self, state_objects):
        for so in state_objects:
            if not isinstance(so, IState):
                raise Exception("state_objects must be collection of IStates.")

    def copy(self):
        return self.__class__([v for (k, v) in self._states.items()])

###
### Bases
###

class StateBase(IState):
    def _copy(self, new):
        pass

    def copy(self):
        new = self.__class__()
        self._copy(new)
        return new


class StateBaseValue(StateBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("init_value", self._valueInit())

    def _valueInit(self):
        return None

    def _valueValid(self, value):
        return True

    def _valueCopy(self, value):
        return value.copy()

    def _copy(self, new):
        super()._copy(new)
        new.value = self._valueCopy()

    def value():
        doc = "The value property."
        def fget(self):
            return self._value
        def fset(self, v):
            if not self._valueValid(v):
                raise Exception("ParseStateConstantValue: Bad value.")
            self._value = v
        def fdel(self):
            del self._value
        return locals()
    value = property(**value())
 

class StateBaseStack(StateBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._stack = list(kwargs.get("init_stack", []))

    @classmethod
    def _validStackElement(cls, value):
        return True

    @classmethod
    def _copyStackElement(cls, element):
        return element

    def _copy(self, new):
        super()._copy(new)
        new._stack = list(map(self._copyStackElement, self._stack))

    def push(self, value):
        if not self._validStackElement(value):
            raise Exception("StateStack: Bad stack value.")
        self._stack.append(value)

    def pop(self):
        return self._stack.pop()

    @property
    def top(self):
        if len(self._stack) == 0:
            return None
        return self._stack[-1]

    @property
    def bottom(self):
        if len(self._stack) == 0:
            return None
        return self._stack[0]

###
### Metamods
###

def StateMetaModKey(base, state_key):
    @classmethod
    def key(cls):
        return state_key
    return base.__class__("_GEN_StateMetaModKey", (base,), locals())


def StateMetaModClassKey(base):
    @classmethod
    def key(cls):
        return cls
    return base.__class__("_GEN_StateMetaModClassKey", (base,), locals())
