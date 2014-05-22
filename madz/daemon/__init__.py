import madz.bootstrap
from .IMinion import *

@madz.bootstrap.manager
class Minion(madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IMinion
    
    class identity(madz.bootstrap.LookupComponentIndex):
        def key(self, plugin):
            return plugin.identity()
madz.bootstrap.index(Minion)(Minion.identity)

from .Daemon import *
from .minions import *

from . import client