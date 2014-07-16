from abc import *


class INodeCoerce(metaclass=ABCMeta):
    """Provides functionality for coercing nodes in the graph to provide useful information."""
    
    @abstractmethod
    def graph_coerce_node(self, node):
        """Given a node, coerce it into an object usable by the graph. 
        
        Node must support equality, hashing, and ordering.
        
        All other graph functions will pass nodes after calling this function on them.
        """
        
        pass
        
    @abstractmethod
    def graph_node_edges(self, node):
        """Computes outgoing and incoming edges of node.
        
        Args:
            node : object on which graph_coerce_node was called 
            
        Returns:
            Tuple of Dictionaries, the first containing incoming edges, the other outgoing edges
        """
        
        pass
        
    @abstractmethod
    def graph_list_nodes(self):
        """Returns an enumerable (list, set, generator, etc) of every node (pre coerce) in the graph.
        
        Returning None implies that graph algorithms provided by a class are intended to function in a subclass
        """
        pass
        
        