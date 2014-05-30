"""pydynecs/abstract/IManagerKey.py
@OffbyOne Studios 2014
Description of an object which provides a key for managers in a system.
"""
import abc

class IManagerKey(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def pydynecs_key(self):
        """An object which is the key to use as the manager key.
        """
        pass
