from abc import *


class ITraversal(metaclass=ABCMeta):

    @abstractmethod
    def path(self):
        """Return the list of edges to reach the current location."""
        pass
    
    @abstractmethod   
    def walk(self): 
        """Return the list of nodes to reach the current location (including current and root node)."""
        pass
    
    @abstractmethod
    def is_leaf(self):
        """ Computes if this node is a leaf (no outgoing edges)."""
        pass
        
    @abstractmethod
    def graph(self):
        """The current graph."""
        pass
    
    @abstractproperty  
    def node(self):
        """The current node."""
        pass
        
    @abstractproperty
    def edge(self):
        """The edge which arrived us at this node."""
        pass
    
    @abstractproperty
    def weight(self):
        """The accumulated weight after arriving at this node (includes this nodes weight)."""
        pass
        
    @abstractproperty
    def set_out_edges(self, edge_dict):
        """Inform the traversal about the outgoing edges acceptable for traversing out of this node.
        
        This effects the is_leaf function on this class). 
        
        Args:
            edge_dict dictionary mapping destination objects (pre coerce) to edge data, using the current node as the source for each edge.
        """
        pass
        
        
        
class BreadthTraversal(ITraversal):
    """Traversal which steps in Breadth First order"""
    pass
    
class DepthTraversal(ITraversal):
    """Traversal which steps in Depth First order"""
    pass
    
    
