from .IEntity import *
from .IEntityAllocator import *

from .IEntityManager import *
from .IComponentManager import *
from .IIndexManager import *

from .ISystem import *

def entity(e):
    while isinstance(e, IEntity):
        e = e.entity_id()
    return e