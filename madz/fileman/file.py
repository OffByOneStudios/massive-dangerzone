import os
import os.path as path

import re

from .core import *

@manager
class File(EntityToComponentManager, EntityClass):
    depends = [Path]
    component_name = "is_file"
    def has_entity(self, entity):
        e = self.s(entity)
        if not Path in e: return False
        p = e[Path]
        return (not os.path.exists(p)) or os.path.isfile(p)

    @entity_property
    def pyopen(s, e, *args, **kwargs):
        e = s(e)
        e.parent.ensure()
        return open(s[Path][e], *args, **kwargs)
    