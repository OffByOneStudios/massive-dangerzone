import tkinter as tk

import madz.bootstrap

from .ITool import *
from . import *

@madz.bootstrap.bootstrap_plugin("tools.core.ToolChooser")
class ToolChooser(ITool):
    class TKinter(tk.Toplevel):
        def __init__(self, controller, master=None):
            self._controller = controller
            
            super().__init__(master)
            
            self.title(self._controller.identity())
            for plugin in madz.bootstrap.EcsBootstrap[Tool].entities():
                plugin = madz.bootstrap.Entity(plugin)
                b = tk.Button(self, text=plugin[madz.bootstrap.Name], command=self._controller.spawn)
                b.grid()
    
    ### START ITool
    
    @classmethod
    def identity(cls):
        return "ToolChooser"
    
    def tkinter_toplevel(self, *args, **kwargs):
        if self._toplevel is None:
            self._toplevel = self.TKinter(self, *args, **kwargs)
        return self._toplevel
    
    def minion_clients(self):
        return []
    
    ### END ITool
    
    def __init__(self):
        self._toplevel = None
    
    def spawn(self):
        launch(madz.bootstrap.EcsBootstrap[Tool.identity][self.identity()])
        