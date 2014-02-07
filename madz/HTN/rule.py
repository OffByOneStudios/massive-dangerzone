from abc import *

from .state import *
from .terms import *

###
### Abstract Bases
###

class IMethod(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    @property
    @abstractmethod
    def term_typenames(self):
        """Set of terms this method can resolve."""
        pass

    @abstractmethod
    def precondition(self, term, state):
        """Returns None (or false) if this method can't be applied, otherwise
        returns an object specific to this method.

        Cannot modify state object.
        """
        pass

    @abstractmethod
    def postcondition(self, term, state, precond_object):
        """Applies post condition to state. Given precondition object."""
        pass

    @abstractmethod
    def execute(self, execute_state, precond_object):
        """Actually executes the method. The execute_state is modified
        to generate the results. Given precondition object."""
        pass

###
### Bases
###

class MethodBase(IMethod):
    def __nop(self, es):
        pass

    def __init__(self, **kwargs):
        self._terms = kwargs.get("terms", set())
        self._action = kwargs.get("action", self.__nop)

    @property
    def term_typenames(self):
        return self._terms

    def _generateExpandedTerms(self):
        return []

    def precondition(self, term, state):
        return locals()

    def postcondition(self, term, state, precond_object):
        state[TermsState.key()].expandCurrentTerm(
            with_terms=self._generateExpandedTerms(),
            current_term=state[TermsState.key()].current_term)

    def execute(self, execute_state, precond_object):
        self._action(execute_state)


class MethodBaseComplex(MethodBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._expand_terms = list(kwargs.get("expand_terms", []))

    def _generateExpandedTerms(self):
        return self._expand_terms

###
### Concrete
###

class MethodPrimitive(MethodBase):
    pass

