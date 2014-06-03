from PyQt4 import QtCore, QtGui

import pydynecs

# From: http://www.hardcoded.net/articles/using_qtreeview_with_qabstractitemmodel
class AbstractTreeModel(QtCore.QAbstractItemModel):
    def __init__(self):
        QAbstractItemModel.__init__(self)
    
    def get_root_node(self, row):
        raise NotImplementedError()
    
    def get_root_count(self):
        raise NotImplementedError()
    
    def get_sub_node(self, base_node, row):
        raise NotImplementedError()
    
    def get_node_row(self, node):
        raise NotImplementedError()
    
    def index(self, row, column, parent):
        if not parent.isValid():
            res_node = self.root_node(row)
        else:
            base_node = parent.internalPointer()
            res_node = self.get_sub_node(base_node, row)
        return self.createIndex(row, column, res_node)
    
    def parent(self, index):
        if not index.isValid():
            return None
        node = index.internalPointer()
        parent_node = self.get_parent(self, node)
        if parent_node is None:
            return None
        else:
            return self.createIndex(self.get_node_row(parent_node), 0, parent_node)
    
    def rowCount(self, parent):
        if not parent.isValid():
            return self.get_root_count()
        node = parent.internalPointer()
        return len(self.get_subnodes(node))
    