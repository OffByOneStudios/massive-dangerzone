from abc import *

class IMethod(object):
    __metaclass__ = ABCMeta
    
    @property
    @abstractmethod
    def task_name(self):
        pass

    @abstractmethod
    def precond(self, variables):
        pass

    @abstractmethod
    def task_network(self, variables):
        pass