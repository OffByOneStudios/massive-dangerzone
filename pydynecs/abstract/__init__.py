"""pydynecs/abstract/__init__.py
@OffbyOne Studios 2014
Abstract interfaces used within pydynecs.
"""

from .IEntity import *
from .IEntityAllocator import *

from .IEntityManager import *
from .IReadableComponentManager import *
from .IComponentManager import *
from .IIndexManager import *

from .IEntityClass import *

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
    if k is None: return None
    while not (isinstance(k, str)) and (isinstance(k, IManagerKey) or issubclass(k, IManagerKey)):
        k = k.pydynecs_key()
    return k
