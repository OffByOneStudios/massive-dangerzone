from PyQt4 import QtCore, QtGui

import madz.bootstrap

from .. import PyQtExt
from .ITool import *
from . import *

# From: http://www.gulon.co.uk/2013/01/30/button-delegate-for-qtableviews/
class ButtonDelegate(QtGui.QItemDelegate):
    def __init__(self, parent, namegetter, onclick):
        super().__init__(parent)
        self.namegetter = namegetter
        self.onclick = onclick
 
    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            data = index.data()
            button = QtGui.QPushButton(
                    self.namegetter(data),
                    self.parent(),
                )
            button.clicked.connect(lambda c, d=data, s=self: s.onclick(d))
            self.parent().setIndexWidget(index, button)
    
    def sizeHint(self, option, index):
        return QtGui.QPushButton(self.namegetter(index.data())).sizeHint()

@madz.bootstrap.bootstrap_plugin("tools.core.ToolChooser")
class ToolChooser(ITool):
    class Widget(QtGui.QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.initQt()
        
        def initQt(self):
            self.setWindowTitle(self._controller.identity())
            
            layout = QtGui.QVBoxLayout()
            
            tableData = PyQtExt.EcsTableModel(madz.bootstrap.EcsBootstrap, Tool)
            tableData.setManagers([
                madz.bootstrap.Name,
                Tool,
            ])
            tableData.setConversion(Tool, lambda d, i: d)
            
            self._table = table = QtGui.QTableView()
            
            table.setShowGrid(False)
            table.verticalHeader().setVisible(False)
            table.setModel(tableData)
            table.setItemDelegateForColumn(1,
                ButtonDelegate(table,
                    namegetter=lambda d: None if d is None else d.identity(),
                    onclick=lambda d, s=self: None if d is None else s._controller.spawn(d)))
            
            
            table.resizeColumnsToContents()
            
            layout.addWidget(table)
            self.setLayout(layout)
            
        
    ### START ITool
    
    @classmethod
    def identity(cls):
        return "ToolChooser"
    
    def qtWidgetClass(self):
        return self.Widget
    
    def minion_clients(self):
        return []
    
    ### END ITool
    
    def __init__(self):
        class Widget(ToolChooser.Widget):
            _controller = self
        self.Widget = Widget
        self._toplevel = None
    
    def spawn(self, to_spawn):
        launch(madz.bootstrap.EcsBootstrap[Tool.identity][to_spawn.identity()])
        