"""variables.py
@Offbyonestudios 2014

This application is not web scale.
"""
from abc import *


class IVariable(object):
    """
    """
    __metaclass__ = ABCMeta


    @property
    @abstractmethod
    def is_free(self):
        """Returns true if variable is free."""
        pass

    @property
    @abstractmethod
    def name(self):
        """Return variable name."""
        pass

    @property
    @abstractmethod
    def value(self):
        """Return variable value.

            Remarks:
                returns None if variable if free.
        """
        pass

    @abstractmethod
    def copy(self):
        """Clone this object."""
        pass

    def __hash__(self):
        return hash(self.name)

    def __equals__(self, other):
        if self.is_free and other.is_free:
            return self.name == other.name
        elif self.is_free != other.is_free:
            return False
        else:
            return self.value == other.value and self.name == other.name


class FreeVariable(IVariable):
    """Helper class representing a free variable.
    """

    def __init__(self, name):
        """Construct a FreeVariable with its name.

            Args:
                name : string name of variable.
        """
        self._name = name

    @property
    def is_free(self):
        """Returns true if variable is free."""
        return True

    @property
    def value:
        """Return variable value.

            Remarks:
                returns None if variable if free.
        """
        return None

    @property
    def name(self):
        """Return variable name."""
        return self._name

    def copy(self):
        """Clone this object."""
        return self.__class__(self._name)


class BoundVariable(IVariable):
    """Helper class representing a bound variable.
    """

    def __init__(self, name, value):
        """Construct a Bound variable with its name.

            Args:
                name : string name of variable.
        """
        self._name = name
        self._value = value

    @property
    def is_free(self):
        """Returns true if variable is free."""
        return False

    @property
    def value:
        """Return variable value.

            Remarks:
                returns None if variable if free.
        """
        return None

    @property
    def name(self):
        """Return variable name."""
        return self._name

    def set_value(self, value):
        """Clone this variable with new value.

            Args:
                value : new value.

        """
        return self.__class__(self._name, value)

    def copy(self):
        """Clone this object."""
        return self.__class__(self._name, self._value)
