import sys
import importlib, pkgutil

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

def main_shutdown():
    
    import madz.module
    import madz.fileman
    import madz.report
    
    madz.module.EcsModules.current.stop()
    madz.fileman.EcsFiles.current.stop()
    madz.report.EcsReports.current.stop()

def connect_replicated_ecs():
    import pydynecs
    import madz.daemon.core as daemon
    
    client = daemon.Client()
    
    import madz.module
    import madz.fileman
    import madz.report
    
    madz.module.EcsModules.current = pydynecs.SyncOnDemandClientSystem(
        madz.module.EcsModules,
        *client.invoke_minion("ecsreplicator", ("start-system", "modules")))
    madz.module.EcsModules.current.start()
    madz.fileman.EcsFiles.current = pydynecs.SyncOnDemandClientSystem(
        madz.fileman.EcsFiles,
        *client.invoke_minion("ecsreplicator", ("start-system", "files")))
    madz.fileman.EcsFiles.current.start()
    madz.report.EcsReports.current = pydynecs.SyncOnDemandClientSystem(
        madz.report.EcsReports,
        *client.invoke_minion("ecsreplicator", ("start-system", "reports")))
    madz.report.EcsReports.current.start()

def refresh_tools():
    import madzgui.tools
    for p in pkgutil.walk_packages(madzgui.tools.__path__, madzgui.tools.__name__ + "."):
        try:
            importlib.import_module(p[1])
        except:
            pass

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
    
    if do_main:
        r = qtApp.exec_()
        main_shutdown()
        sys.exit(r)
