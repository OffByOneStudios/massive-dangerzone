import madz
import madz.module

from PyQt4 import QtCore, QtGui
from madzgui import PyQtExt

class BrowserWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.initQt()
    
    def initQt(self):
        self.setWindowTitle(self._controller.identity())
        
        layout = QtGui.QVBoxLayout()
        
        tableData = PyQtExt.EcsTableModel(madz.module.EcsModules, madz.module.Id)
        tableData.setManagers([
            madz.module.Id,
            madz.module.FileModuleRelationFileEntity,
        ])
        tableData.setConversion(madz.module.Id, lambda d, i: str(d))
        tableData.setConversion(madz.module.FileModuleRelationFileEntity, lambda d, i: repr(d))
        
        self._table = table = QtGui.QTableView()
        
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.setModel(tableData)
        
        table.resizeColumnsToContents()
        
        layout.addWidget(table)
        self.setLayout(layout)