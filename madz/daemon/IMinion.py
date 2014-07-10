import abc

class IMinion(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def minion_spawn(self):
        pass

    @abc.abstractmethod
    def minion_banish(self):
        pass

    @classmethod
    @abc.abstractmethod
    def minion_identity(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def minion_index(cls):
        """Returns helper objects and an index of of features for a minion (or None)"""