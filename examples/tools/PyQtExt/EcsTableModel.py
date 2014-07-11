from PyQt4 import QtCore, QtGui

import pydynecs

#TODO use pydynecs casting methods
class EcsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, system, entity_manager, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        system = system.current
        
        self._system = system
        self._entity_manager = system[entity_manager]
        
        self._actual_managers = None
        self._resolveManagers()
        
        self._cache_entities = list(self._entity_manager.entities())
        
        self._conversions = {}
    
    def _resolveManagers(self):
        if self._actual_managers == None:
            self._cache_managers = list(self._system.managers())
        else:
            self._cache_managers = self._actual_managers
    
    def _viewConvert(self, manager_key, data, index):
        if manager_key in self._conversions:
            return self._conversions[manager_key](data, index)
        return str(data)
    
    def setManagers(self, managers):
        self._actual_managers = list(map(lambda m, s=self: (m, s._system[m]), managers))
        self._resolveManagers()
    
    def setConversion(self, manager_key, func):
        self._conversions[manager_key] = func
    
    def columnCount(self, parent):
        return len(self._cache_managers)

    def rowCount(self, parent):
        return len(self._cache_entities)
    
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        
        entity = self._cache_entities[index.row()]
        (key, manager) = self._cache_managers[index.column()]
        
        if entity in manager:
            return self._viewConvert(key, manager[entity], index)
        else:
            return None
    
    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole: 
            return None
        
        if orientation == QtCore.Qt.Horizontal:
            return str(self._cache_managers[section][0].__name__)
        elif orientation == QtCore.Qt.Vertical:
            return str(pydynecs.entity(self._cache_entities[section]))
        else:
            return None
