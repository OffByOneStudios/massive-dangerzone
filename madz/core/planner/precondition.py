"""precondition.py
@Offbyonestudios 2014
Object which constructs a possible set of bound variables for a method using 
"""

from abc import *



class IPrecondition(object):
    """
    """
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def free_variables(self):
        """Return string names of free variables."""
        pass

    @property
    @abstractmethod
    def bound_variables(self):
        """Return string names of bound variables."""
        pass
    
    @property
    def all_variables(self):
        """Returns string names of all variables"""
        return set(self.bound_variables) | set(self.free_variables)

    @abstractmethod
    def bind(self, bound_variables):
        """Uses bound_variables to return all possibel bindings the free variables

            Remarks:
                Might be a generator.

            Args:
                bound_variables : set of bound variables

            Returns:
                Set of all Poossible bindings of free variables
        """
        pass


class PreconditionOr(IPrecondition)
    """A Set of Preconditions"""


    def __init__(self, preconditions):
        """constructs a precondition set with its preconditions"""
        self._preconditions = set(preconditions)

    @property
    def free_variables(self):
        """Return string names of free variables."""
        return set([v for l in self.preconditions for v in l.free_variables])

    @property
    def bound_variables(self):
        """Return string names of bound variables."""
        return set([v for l in self.preconditions for v in l.bound_variables])
