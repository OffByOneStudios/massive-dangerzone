"""madz/start_mode/core/__init__.py
@OffbyOne Studios 2014
Core startmode features.
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

import madz.bootstrap

@madz.bootstrap.manager
class StartMode(madz.bootstrap.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IStartMode

@madz.bootstrap.manager
class StartMode_identity(madz.bootstrap.LookupIndexManager):
    source = StartMode
    def key(self, plugin):
        return self.s[StartMode][plugin].startmode_identity()

def get_start_mode(name):
    if name in StartMode_identity.current:
        return StartMode_identity.current[name][StartMode]
    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madz.start_mode.{}".format(name))
        try:
            return StartMode_identity.current[name][StartMode]
        except:
            pass
        return plugin[madz.bootstrap.Object]
