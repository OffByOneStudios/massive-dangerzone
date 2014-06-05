#include ".madz/cpp/.wrap-cpp/madz.h" //"madz.h" would also work.
#include <iostream>

// Internal Class Definition
class GizmoInternal{
private:
    int32_t biz;
public:

    GizmoInternal(int32_t biz_in)
    {
        biz = biz_in;
    }
    
    int32_t add(int32_t foo)
    {
        return biz + foo;
    }
};

// Initialization Function.
void MADZOUT::_init() {
    std::cout << "task.cpp Init\n";
}

MADZOUT::_t::Gizmo MADZOUT::_f::Gizmo_create(int32_t biz)
{
    GizmoInternal* res = new GizmoInternal(biz);
    return (MADZOUT::_t::Gizmo)res;
}

void MADZOUT::_f::Gizmo_destroy(MADZOUT::_t::Gizmo gizmo)
{
    GizmoInternal* del = (GizmoInternal*)gizmo;
    delete del;
}

int32_t MADZOUT::_f::Gizmo_add(MADZOUT::_t::Gizmo gizmo, int32_t foo)
{
    GizmoInternal* obj = (GizmoInternal*)gizmo;
    return obj->add(foo);
}
