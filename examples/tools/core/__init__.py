import sys

import pydynecs

import madz.bootstrap
from .ITool import *

@madz.bootstrap.manager
class Tool(pydynecs.ObservableComponentManager, madz.bootstrap.BootstrapPluginImplementationComponentManager):
    interface = ITool
    
    class identity(madz.bootstrap.LookupIndexManager):
        def key(self, plugin):
            return madz.bootstrap.EcsBootstrap[Tool][plugin].identity()

from PyQt4 import QtGui
qtApp = None
def launch(tool_plugin):
    global qtApp
    
    do_main = False
    if qtApp is None:
        qtApp = QtGui.QApplication(sys.argv)
        do_main = True
    
    tool = madz.bootstrap.Entity(tool_plugin)[Tool]()

    window = tool.qtWidgetClass()()
    
    window.show()
    
    if do_main:
        sys.exit(qtApp.exec_())

from .ToolChooser import *