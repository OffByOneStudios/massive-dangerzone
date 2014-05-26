import madz.bootstrap
from .ITool import *

@madz.bootstrap.manager
class Tool(madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = ITool
    
    class identity(madz.bootstrap.LookupComponentIndex):
        def key(self, plugin):
            return plugin.identity()
madz.bootstrap.index(Tool)(Tool.identity)

tkinter_root = None
def launch(tool_plugin):
    import tkinter as tk
    
    do_main = False
    if tkinter_root is None:
        global tkinter_root
        tkinter_root = tk.Tk()
        tkinter_root.wm_withdraw()
        do_main = True
    
    tool = madz.bootstrap.Entity(tool_plugin)[Tool]()

    frame = tool.tkinter_toplevel(master=tkinter_root)
    
    if do_main:
        tkinter_root.mainloop()

from .ToolChooser import *