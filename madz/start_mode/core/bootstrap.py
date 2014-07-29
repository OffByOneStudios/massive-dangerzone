"""madz/start_mode/core/bootstrap.py
@OffbyOne Studios 2014
Bootstrap startmode features.
"""

import madz.bootstrap
from . import *

@madz.bootstrap.manager
class StartMode(madz.bootstrap.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IStartMode

@madz.bootstrap.manager
class StartMode_identity(madz.bootstrap.LookupIndexManager):
    source = StartMode
    def key(self, plugin):
        return self.s[StartMode][plugin].startmode_identity()
