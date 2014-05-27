import abc

class ITool(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def identity(cls):
        """Tool identity."""
        pass
    
    @abc.abstractmethod
    def qtWidgetClass(self):
        """Returns a qtWidget class for this tool instance."""
        pass
    
    @abc.abstractmethod
    def minion_clients(self):
        """Returns a list of IMinionClient s."""
        pass
