from abc import *

from . import inode

class GraphBase(inode.INodeCoerce):
    pass
    
    
class IWeightedEdgeGraph(metaclass=ABCMeta):
    """Some functions require weighted edges. Every edge is assumed to weight 1 unless this interface is provided.
    """
    @abstractmethod
    def graph_edge_weight(self, src, dst, edge):
        """Given the source node, destination node and edge data compute a comparable weight value. 
        
            Weight values must support equality, hashing, ordering, and addition.
        """
        pass
        
    @abstractmethod
    def graph_limits(self):
        """Returns a dictionary of limits on edges in this graph space in a dictionary.
            This dictionary merges with other graph_limits functions.
        """
        pass
        
class IWeightedNodeGraph(metaclass=ABCMeta):
    """Some functions require weighted nodes. Every node is assumed to weight 0 unless this interface is provided.    
    """

    @abstractmethod
    def graph_node_weight(self, node):
        """Given a node, compute a comparable weight value. 
            Weight values must support equality, hashing, ordering, and addition.
        """
        pass
        
    @abstractmethod
    def graph_limits(self):
        """Returns a dictionary of limits on nodes in this graph space in a dictionary.
            This dictionary merges with other graph_limits functions.
        """
        pass
        