"""madz/start_mode/core/IStartMode.py
@OffbyOne Studios 2014
Abstract startmode features.
"""

import abc

class IStartMode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def startmode_start(self, argv, system, user_config):
        pass

    @classmethod
    @abc.abstractmethod
    def startmode_identity(self):
        pass

