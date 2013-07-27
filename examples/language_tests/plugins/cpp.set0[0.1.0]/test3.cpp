#include "header.h"

void test3_init()
{
    test3_var0 = 0.0;
    test3_var1 = 1.0;
    test3_var_pointer = &test3_var0;
}

void MADZOUT::_f::test3_func() {
    test3_var_pointer = &test3_var1;
}
