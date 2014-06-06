"""core/plugin_directory.py
@OffbyOne Studios 2013
Provides plugin directory objects for loading plugins.
"""
import os

from .. import fileman

@fileman.manager
class File_ModuleEntity(fileman.CheckedComponentManager, fileman.BasicComponentManager, fileman.EntityClass):
    depends=[fileman.Path, fileman.Directory]
    component_name="madz_module"
    def check(self, value):
        return isinstance(value, PluginStub)
    
    @fileman.entity_property
    def madz(s, e):
        if not s[fileman.Directory].has_entity(e):
            raise Exception("Madz directory can only exist for MadzPluginPaths which are directories")
        return e.dir(".madz")

from .plugin_stub import *