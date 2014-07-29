"""madz/daemon/minion/core/boostrap.py
@OffbyOne Studios 2014
Bootstrap minion features.
"""

import madz.bootstrap
from . import *

@madz.bootstrap.manager
class Minion(madz.bootstrap.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IMinion

@madz.bootstrap.manager
class Minion_identity(madz.bootstrap.LookupIndexManager):
    source = Minion
    def key(self, plugin):
        return self.s[Minion][plugin].minion_identity()