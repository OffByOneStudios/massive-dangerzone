#include ".madz/c/.wrap-c/madz.h" //"madz.h" would also work.

#include <stdio.h>

typedef struct{
    int32_t biz;
} GizmoInternal;

MADZINIT {
    printf("task.c Init\n");
}

MADZOUTFUNC_Gizmo_create{
    GizmoInternal* res = malloc(sizeof(GizmoInternal));
    res->biz = biz;
    return (___madz_TYPE__Gizmo)res;
}

MADZOUTFUNC_Gizmo_destroy{
    GizmoInternal* del = (GizmoInternal*)gizmo;
    free(del);
}

MADZOUTFUNC_Gizmo_add{
    GizmoInternal* obj = (GizmoInternal*)gizmo;
    return obj->biz + foo;
}
