from ctypes import *
from abc import *
import hashlib
import logging
import os
import os.path as path

from .file import File
from .core import *

logger = logging.getLogger(__name__)

@manager
class Directory(EntityToComponentManager, EntityClass):
    depends = [Path, Path_lookup]
    component_name = "is_directory"
    def has_entity(self, entity):
        e = self.s(entity)
        if not Path in e: return False
        p = e[Path]
        return (not os.path.exists(p)) or os.path.isdir(p)

    @entity_property
    def contents(s, e):
        if not Path.exists(s, e):
            return list()
        to_file = Directory.file
        return list(map(lambda p: to_file(s, e, p), os.listdir(s[Path][e])))

    @entity_property
    def file(s, e, *args):
        return s[Path_lookup][os.path.join(s[Path][e], *args)]

    @entity_property
    def list(s, e, exts=[], wdirs=False, wfiles=True):
        e = s(e)
        dir = e[Path]

        isdir = s[Directory]
        isfile = s[File]

        files = []
        for f in e.contents():
            if Path.extension(s, f) in exts:
                if (wdirs and isdir[f]) or (wfiles and isfile[f]):
                    files.append(f)
        return files

    @entity_property
    def dir(s, e, *args):
        return s[Path_lookup][os.path.join(s[Path][e], *args)]

    @entity_property
    def ensure(s, e):
        p = s[Path][e]
        if not os.path.exists(p):
            os.makedirs(p)
