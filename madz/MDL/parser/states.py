from .abstract_bases import *

class ParseStateConstantBase(IParseState):
    def copy(self):
        return self

class ParseStateSpecialRules(ParseStateClassKeyMetaMod(ParseStateConstantBase)):
    def __init__(self, whitespace, comment):
        super().__init__()
        self.whitespace = whitespace
        self.comment = comment

    def all(self):
        return [
            self.whitespace,
            self.comment
        ]

class ParseStateParseTree(ParseStateClassKeyMetaMod()):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.roots = []
        self.current_root = None
        self._current_func = None

    @classmethod
    def _valid_root(cls, root):
        return cls._valid_node(root)

    @classmethod
    def _valid_node(cls, node):
        return True

    def add_root(self, root=None):
        if (root is None):
            root = self.current_root
            self.current_root = None
            self._current_func = None
        self.roots.append(root)

    def current_root():
        doc = "The current root being generated."
        def fget(self):
            return self._current_root
        def fset(self, value):
            if not self._valid_root(value):
                raise ValueError("Root not valid.")
            self._current_root = value
        def fdel(self):
            del self._current_root
            del self._current_func
        return locals()
    current_root = property(**current_root())

    def set_current_node_func(self, func):
        """Set the func that uses the root node to retrieve the current node"""
        self._current_func = func

    def current_node():
        doc = "The current node being generated."
        def fget(self):
            if self._current_func is None:
                return None
            return self._current_func(self.current_node)
        return locals()
    current_node = property(**current_node())

    def __str__(self):
        return "\n".join(
            map(repr, self.roots))

    def _copy(self, new):
        super()._copy(new)
        new.roots = list(map(lambda r: r, self.roots)) #TODO Copy
        new.current_root = None if self.current_root is None else self.current_root #TODO Copy
        new._current_func = self._current_func
