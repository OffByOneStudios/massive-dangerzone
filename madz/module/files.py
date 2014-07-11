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
        module_relation = EcsModules.current[FileModuleRelationFileEntity]
        if not self.module in module_relation:
            module_relation[self.module] = {}
        module_relation[self.module][self.file] = self
    
class FileModuleRelationshipModuleDirectory(FileModuleRelationship):
    pass

class FileModuleRelationshipDescriptionFile(FileModuleRelationship):
    pass

class FileModuleRelationshipSourceFile(FileModuleRelationship):
    pass

class FileModuleRelationshipGeneratedFile(FileModuleRelationship):
    pass

class FileModuleRelationshipGeneratedCacheFile(FileModuleRelationship):
    pass

## Files

@fileman.manager
class FileModuleRelationModuleEntity(fileman.BasicComponentManager, fileman.EntityClass):
    depends=[fileman.Path]
    component_name="madz_module"

class FileModuleRelationFileBase(fileman.IEntityManager):
    relationship_class=FileModuleRelationship
    
    def has_entity(self, entity):
        return (self.s[FileModuleRelationModuleEntity].has_entity(entity)
            and isinstance(self.s[FileModuleRelationModuleEntity][entity], self.relationship_class))
            
@fileman.manager
class FileModuleRelationFileModuleDirectory(fileman.EntityClass, FileModuleRelationFileBase):
    relationship_class=FileModuleRelationshipModuleDirectory

    @fileman.entity_property
    def madz(s, e):
        return e.dir(".madz")

## Modules

@manager
class FileModuleRelationFileEntity(BasicComponentManager, EntityClass):
    component_name="files"

class FileModuleRelationModuleBase(IEntityManager):
    relationship_class=FileModuleRelationship
    
    def has_entity(self, entity):
        return (self.s[FileModuleRelationFileEntity].has_entity(entity)
            and isinstance(self.s[FileModuleRelationFileEntity][entity], self.relationship_class))

@manager
class FileModuleRelationModuleModuleDirectory(fileman.EntityClass, FileModuleRelationModuleBase):
    relationship_class=FileModuleRelationshipModuleDirectory

    def directory(s, e):
        return fileman.EcsFiles.current[fileman.Path][s[FileModuleRelationFileEntity][e]]
