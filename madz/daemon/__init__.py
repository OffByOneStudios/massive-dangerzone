import pydynecs

import madz.bootstrap
from .IMinion import *

@madz.bootstrap.manager
class Minion(pydynecs.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IMinion
    
    class identity(madz.bootstrap.LookupIndexManager):
        def key(self, plugin):
            return madz.bootstrap.EcsBootstrap[Minion][plugin].identity()

from .Daemon import *
from .minions import *

from . import client