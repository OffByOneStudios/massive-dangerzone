"""pydynecs/abstract/__init__.py
@OffbyOne Studios 2014
Abstract interfaces used within pydynecs.
"""

from .Entity import *

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
    _e = e
    while isinstance(_e, IEntity):
        _e = _e.entity_id()
    if isinstance(_e, Entity):
        return _e
    raise TypeError("Not coercable to entity: {}".format(e))

def system(s):
    if isinstance(s, ISystem):
        return s
    elif issubclass(s, ISystem):
        return s.current
    raise TypeError("Not coercable to system: {}".format(e))

def manager(s, m):
    if isinstance(m, IEntityManager):
        return m
    return s[m]

def manager_key(k):
    if k is None: return None
    while not (isinstance(k, str)) and (isinstance(k, IManagerKey) or issubclass(k, IManagerKey)):
        k = k.pydynecs_key()
    return k
