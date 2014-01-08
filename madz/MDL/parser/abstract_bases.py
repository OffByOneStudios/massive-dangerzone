from abc import *

###
### Interfaces
###

class IParseResult(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def valid(self):
        """If this parse is valid"""
        pass

    @property
    @abstractmethod
    def error(self):
        """The error or exception encountered"""
        pass

    @property
    @abstractmethod
    def state(self):
        """The new state after this parse"""
        pass

    @property
    @abstractmethod
    def rule(self):
        """The rule generating this."""
        pass

    @property
    @abstractmethod
    def parsed_string(self):
        """The string parsed"""
        pass

    @property
    @abstractmethod
    def new_level(self):
        """The new level to add, if not None."""
        pass

class IParseRule(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def try_parse(self, pstr, state):
        """Tries the parse, fails quickly, returning None, otherwise returns IParseResult."""
        pass

class IParseState(object):
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

    @staticmethod
    def copy_state(state):
        return {k: v.copy() for k, v in state.items()}

###
### Bases
###
class ParseStateBase(IParseState):
    def _copy(self, new):
        pass

    def copy(self):
        new = self.__class__()

        self._copy(new)
        return new

def ParseStateClassKeyMetaMod(base=ParseStateBase):
    @classmethod
    def key(cls):
        return cls
    def __init__(self, **kwargs):
        super(base, self).__init__(**kwargs)
    return base.__class__("_GEN_ParseStateClassKeyMod", (base,), locals())

class ParseStateValue(ParseStateClassKeyMetaMod()):
    def __init__(self):
        super().__init__()
        self.value = self._value_init()

    def _copy(self, new):
        super()._copy(new)
        new.value = self._value_copy()

    def value():
        doc = "The value property."
        def fget(self):
            return self._value
        def fset(self, v):
            if not self._value_valid(v):
                raise Exception("ParseStateConstantValue: Bad value.")
            self._value = v
        def fdel(self):
            del self._value
        return locals()
    value = property(**value())

class ParseStateStack(ParseStateClassKeyMetaMod()):
    def __init__(self):
        super().__init__()
        self._stack = []

    @classmethod
    def _valid_value(cls, value):
        return True

    def _copy(self, new):
        super()._copy(new)
        new._stack = list(self._stack)

    def push(self, value):
        if not self._valid_value(value):
            raise Exception("ParseStateStack: Bad stack value.")
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

class ParseResult(IParseResult):
    def __init__(self, _str, _valid=True, _error=None, _state=None, _new_level=None, _rule=None, **kwargs):
        self._str = _str
        self._valid = _valid
        self._state = _state
        self._error = _error
        self._new_level = _new_level
        self._rule = _rule

    @property
    def valid(self):
        return self._valid

    @property
    def error(self):
        return self._error

    @property
    def state(self):
        return self._state

    @property
    def rule(self):
        return self._rule

    @property
    def parsed_string(self):
        return self._str

    @property
    def new_level(self):
        return self._new_level

    def __str__(self):
        if self._valid:
            return "{!s}".format(self._rule)
        else:
            return "{!s}".format(self._error)