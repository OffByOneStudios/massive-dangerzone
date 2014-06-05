import madz

print("task init")



class GizmoInternal(object):
    _prevent_gc_ = dict()
    
    
    def __init__(self, biz):
        self._biz = biz
        GizmoInternal._prevent_gc_[id(self)] = self
        
    def add_foo(self, foo):
        return self._biz + foo
        
        
def Gizmo_create(biz):
    res = GizmoInternal(biz)
    return id(res)
    
def Gizmo_destroy(gizmo):
    GizmoInternal._prevent_gc_[gizmo] = None
    
def Gizmo_add(gizmo, foo):
    return GizmoInternal._prevent_gc_[gizmo].add_foo(foo)

