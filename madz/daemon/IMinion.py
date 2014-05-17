import abc

class IMinion(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def spawn(self):
        pass

    @abc.abstractmethod
    def banish(self):
        pass

    @classmethod
    @abc.abstractmethod
    def identity(cls):
        pass
