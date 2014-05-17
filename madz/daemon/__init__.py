import madz.bootstrap
from .IMinion import *

madz.bootstrap.syntax_manager(
    madz.bootstrap.EcsBootstrap,
    "Minion",
    madz.bootstrap.BootstrapPluginImplementationComponentManager(IMinion))
madz.bootstrap.syntax_index(
    madz.bootstrap.EcsBootstrap,
    Minion,
    "identity",
    madz.bootstrap.LookupComponentIndex(lambda p: p.identity()))

from .Daemon import *
from .minions import *

from . import client