from abc import *

from .state import *

class ITerm(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def typename(self):
        """The name of the type of this term."""
        pass

    @property
    @abstractmethod
    def args(self):
        """The args given to this term."""
        pass

    def __str__(self):
        return "{}({})".format(
            self.typename,
            ", ".join(map(
                lambda s: "{}: {}".format(*s),
                self.args.items()))
        )

    def __repr__(self):
        return "Term({}, {})".format(
            repr(self.typename),
            ", ".join(map(
                lambda s: "{}={}".format(*s),
                self.args.items()))
        )


class Term(ITerm):
    def __init__(self, typename, **kwargs):
        self.args = kwargs
        self.typename = typename

    def typename():
        def fget(self):
            return self._typename
        def fset(self, value):
            self._typename = value
        return locals()
    typename = property(**typename())

    def args():
        def fget(self):
            return self._args
        def fset(self, value):
            self._args = value
        return locals()
    args = property(**args())


class TermsState(StateMetaModClassKey(StateBase)):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._terms = kwargs.get("init_terms", [])

    def _ensureTerm(self, value):
        if not isinstance(value, ITerm):
            raise Exception("Can only use term objects.")

    @property
    def currentTerm(self):
        return self._terms[0]

    def lengthOfTerms(self):
        return len(self._terms)

    def expandCurrentTerm(self, with_terms, current_term=None):
        if (current_term != None) and current_term != self.currentTerm:
            Exception("Cannot replace, top term not correct.")
        for wt in with_terms:
            self._ensureTerm(wt)
        self._terms = list(with_terms + self._terms[1:])

    def _copy(self, new):
        super()._copy(new)
        new._terms = list(self._terms)


