"""madzmodule:module/new/language/core/bootstrap.py
@OffbyOne Studios 2014
Manager for generating new language files.
"""


import madz.bootstrap
from . import *


@madz.bootstrap.manager
class NewLanguage(madz.bootstrap.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = INewLanguage

@madz.bootstrap.manager
class NewLanguage_identity(madz.bootstrap.LookupIndexManager):
    source = NewLanguage
    def key(self, plugin):
        return self.s[NewLanguage][plugin].newlanguage_identity()
