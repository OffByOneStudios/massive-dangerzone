import pydynecs

import madz.bootstrap
from .IMinion import *

daemon_filename = ".madz-daemon"

@madz.bootstrap.manager
class Minion(pydynecs.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IMinion

@madz.bootstrap.manager
class Minion_identity(pydynecs.LookupIndexManager):
    source = Minion
    def key(self, plugin):
        return self.s[Minion][plugin].minion_identity()

from .Daemon import *
from .minions import *

from .Client import *