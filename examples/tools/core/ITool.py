import abc

class ITool(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def identity(cls):
        """Tool identity."""
        pass
    
    @abc.abstractmethod
    def tkinter_toplevel(self, *args, **kwargs):
        """Returns a toplevel Tkinter window."""
        pass
    
    @abc.abstractmethod
    def minion_clients(self):
        """Returns a list of IMinionClient s."""
        pass
