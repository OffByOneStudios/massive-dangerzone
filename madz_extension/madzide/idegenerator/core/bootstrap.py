"""madz/start_mode/core/bootstrap.py
@OffbyOne Studios 2014
Bootstrap startmode features.
"""

import madz.bootstrap
from . import *

@madz.bootstrap.manager
class IdeGenerator(madz.bootstrap.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IIdeGenerator

@madz.bootstrap.manager
class IdeGenerator_identity(madz.bootstrap.LookupIndexManager):
    source = IdeGenerator
    def key(self, plugin):
        return self.s[IdeGenerator][plugin].idegenerator_identity()
