#include "header.h"

void test3_init()
{
    MADZOUT_test3_var0 = 0.0;
    MADZOUT_test3_var1 = 1.0;
    MADZOUT_test3_var_pointer = &MADZOUT_test3_var0;
}

MADZOUTFUNC_test3_func {
    MADZOUT_test3_var_pointer = &MADZOUT_test3_var1;
}
