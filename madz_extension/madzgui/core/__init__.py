import sys

import pydynecs

import madz.bootstrap
from .ITool import *

@madz.bootstrap.manager
class Tool(pydynecs.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = ITool

@madz.bootstrap.manager
class Tool_identity(pydynecs.LookupIndexManager):
    source=Tool
    def key(self, plugin):
        return self.s[Tool][plugin].identity()

from PyQt4 import QtGui
qtApp = None
qtWindows = []
    
def launch(tool_plugin):
    global qtApp
    
    do_main = False
    if qtApp is None:
        qtApp = QtGui.QApplication(sys.argv)
        do_main = True
    
    tool = madz.bootstrap.Entity(tool_plugin)[Tool]()

    class ActualWindow(tool.qtWidgetClass()):
        def closeEvent(self, *args):
            qtWindows.remove(self)
            super().closeEvent(*args)
    
    window = ActualWindow()
    window.show()
    qtWindows.append(window)
    
    print(qtWindows)
    if do_main:
        sys.exit(qtApp.exec_())

from .ToolChooser import *
from .Connector import *