import pydynecs

import madz.bootstrap
from .IMinion import *

@madz.bootstrap.manager
class Minion(pydynecs.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IMinion

@madz.bootstrap.manager
class Minion_identity(pydynecs.LookupIndexManager):
    source = Minion
    def key(self, plugin):
        return self.s[Minion][plugin].identity()

from .Daemon import *
from .minions import *

from . import client