#include "header.h"

void test5_init()
{

}

MADZOUTFUNC_test5_func {
    MADZTYPE(,test5_struct) ret = { .b = b };
    int i;
    for (i = 0; i < 32; i++) {
        ret.a[i] = a[i];
    }
    return ret;
}
