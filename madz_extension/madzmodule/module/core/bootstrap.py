"""madzmodule:module/core/boostrap.py
@OffbyOne Studios 2014
Module Operation Component Manager
"""

import madz.bootstrap
from . import *


@madz.bootstrap.manager
class ModuleOperation(madz.bootstrap.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = IModuleOperation

@madz.bootstrap.manager
class ModuleOperation_identity(madz.bootstrap.LookupIndexManager):
    source = ModuleOperation
    def key(self, plugin):
        return self.s[ModuleOperation][plugin].moduleoperation_identity()
