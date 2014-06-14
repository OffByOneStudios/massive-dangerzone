"""core/files.py
@OffbyOne Studios 2013
Provides relationships between files and plugin managers.
"""
import os

from .. import fileman
        
from .core import *

class FileModuleRelationship(object):
    def __init__(self, file=None, module=None):
        self.module = entity(module)
        self.file = fileman.entity(file)
    
    def build(self):
        fileman.EcsFiles.current[FileModuleRelationModuleEntity][self.file] = self
        EcsModules.current[FileModuleRelationFileEntity][self.module] = self
    
class FileModuleRelationshipModuleDirectory(FileModuleRelationship):
    pass
    
## Files

@fileman.manager
class FileModuleRelationModuleEntity(fileman.BasicComponentManager, fileman.EntityClass):
    depends=[fileman.Path]
    component_name="madz_module"

@fileman.manager
class FileModuleRelationModuleDirectory(fileman.EntityClass):
    def has_entity(self, entity):
        return (self.s[FileModuleRelationModuleEntity].has_entity(entity)
            and isinstance(self.s[FileModuleRelationModuleEntity][entity], FileModuleRelationshipModuleDirectory))

    @fileman.entity_property
    def madz(s, e):
        return e.dir(".madz")

## Modules

@manager
class FileModuleRelationFileEntity(BasicComponentManager, EntityClass):
    component_name="files"

