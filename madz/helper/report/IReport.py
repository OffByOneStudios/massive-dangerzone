
import abc

class IReport(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def report(self):
        pass

    @abc.abstractmethod
    def extend(self, other):
        pass

    def __add__(self, other):
        return self.extend(other)
