from PyQt4 import QtCore, QtGui

import madz

from .ITool import *
from . import *

@madz.bootstrap.bootstrap_plugin("tools.core.Connector")
class Connector(ITool):
    class Widget(QtGui.QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.initQt()
        
        def initQt(self):
            self.setWindowTitle(self._controller.identity())
            
            layout = QtGui.QVBoxLayout()

            self.setLayout(layout)
            
        
    ### START ITool
    
    @classmethod
    def identity(cls):
        return "Connector"
    
    def qtWidgetClass(self):
        return self.Widget
    
    def minion_clients(self):
        return []
    
    ### END ITool
    
    def __init__(self):
        class Widget(self.Widget):
            _controller = self
        self.Widget = Widget
        self._toplevel = None
        