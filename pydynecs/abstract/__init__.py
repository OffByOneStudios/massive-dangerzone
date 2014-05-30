from .IEntity import *
from .IEntityAllocator import *

from .IEntityManager import *
from .IComponentManager import *
from .IIndexManager import *

from .IObservableEntityManager import *

from .IManagerKey import *

from .ISystem import *

def entity(e):
    while isinstance(e, IEntity):
        e = e.entity_id()
    return e

def system(s):
    return s.current

def manager(s, m):
    if isinstance(m, IEntityManager):
        return m
    return s[m]

def manager_key(k):
    while not (isinstance(k, str)) and (issubclass(k, IManagerKey) or isinstance(k, IManagerKey)):
        k = k.pydynecs_key()
    return k
