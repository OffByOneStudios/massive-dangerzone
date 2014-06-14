"""madz/fileman/core.py
@OffbyOne Studios 2014
Core features of the filemanager system.
"""

import abc
import os
import os.path as path
import hashlib
from datetime import datetime
import warnings

from pydynecs import *

@system_syntax
class EcsFiles(System): pass
EcsFiles.current = EcsFiles()
manager = manager_decorator_for(EcsFiles)

@manager
class Path(ObservableComponentManager, CoercingComponentManager, BasicComponentManager, EntityClass):
    component_name = "path"
    def coerce(self, value): return os.path.abspath(value)

    @entity_property
    def exists(s, e):
        return os.path.exists(s[Path][e])

    @entity_property
    def extension(s, e):
        parts = os.path.basename(s[Path][e]).split(".")
        return "" if len(parts) < 1 else parts[-1]

    @entity_property
    def with_extension(s, e, ext):
        path = s[Path][e][:-len(Path.extension(s, e))] + ext
        return s[Path_lookup][path]

    @entity_property
    def fullname(s, e):
        return os.path.basename(s[Path][e])

@manager
class Path_lookup(CoercingIndexManager, CreateOnFailureIndexManager, LookupIndexManager):
    source=Path
    def coerce(self, key): return os.path.abspath(key)

    def create(self, key):
        e = self.s.new_entity()

        self.s[Path][e] = key
        return e

    def key(self, entity):
        return self.s[Path][entity]

@manager
class ParentDirectory(ComputedComponentManager):
    component_name = "parent"
    depends = [Path, Path_lookup]
    def compute(self, entity):
        return self.s[Path_lookup][os.path.dirname(self.s[Path][entity])]

def new(path):
    return EcsFiles.current[Path_lookup][path]
