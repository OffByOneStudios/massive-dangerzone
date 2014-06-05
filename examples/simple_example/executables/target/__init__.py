import madz
def main():
    print("Staring Main...")
    
    c_gizmo = madz.imports["task.c"].Gizmo_create(1)
    cpp_gizmo = madz.imports["task.cpp"].Gizmo_create(2)
    python_gizmo = madz.imports["task.python"].Gizmo_create(3)
    
    print("c_add_foo:", madz.imports["task.c"].Gizmo_add(c_gizmo, 1))
    print("cpp_add_foo:", madz.imports["task.cpp"].Gizmo_add(cpp_gizmo, 2))
    print("python_add_foo:", madz.imports["task.python"].Gizmo_add(python_gizmo, 3))
    
    madz.imports["driver"].do_driver()
    
    madz.imports["task.c"].Gizmo_destroy(c_gizmo)
    madz.imports["task.cpp"].Gizmo_destroy(cpp_gizmo)
    madz.imports["task.python"].Gizmo_destroy(python_gizmo)
    
    exit(0)