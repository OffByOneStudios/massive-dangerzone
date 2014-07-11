
import madz.bootstrap

from ..core import ITool
from .BrowserWidget import *

@madz.bootstrap.bootstrap_plugin("tools.module_browser.Core")
class ModuleBrowserCore(ITool):

    ### START ITool
    
    @classmethod
    def identity(cls):
        return "ModuleBrowser"
    
    def qtWidgetClass(self):
        return self.Widget
    
    def minion_clients(self):
        return []
    
    ### END ITool
    
    def __init__(self):
        class Widget(BrowserWidget):
            _controller = self
        self.Widget = Widget
        self._toplevel = None