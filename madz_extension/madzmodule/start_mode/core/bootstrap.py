"""madzmodule:start_mode/core/boostrap.py
@OffbyOne Studios 2014
Module Startmode Component Manager
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
