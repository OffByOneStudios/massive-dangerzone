from .. import abstract
from . import *

class NodeType(abstract.INodeType):
    def __init__(self, system):
        self._system = system

    def system(self):
        return self._system

    def node(self, entity):
        return Node(self, entity)

    def expand(self, entity):
        pass
