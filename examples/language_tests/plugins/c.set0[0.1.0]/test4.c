#include "header.h"

void test4_init()
{
    MADZOUT_test4_var_simple = 1;

    MADZOUT_test4_var_struct = (MADZTYPE(,test4_type_struct)){ .var = 1, .varp = 0 };
    MADZOUT_test4_var_struct.varp = &(MADZOUT_test4_var_struct.var);

    int i;
    for (i = 0; i < 16; i++) {
        MADZOUT_test4_var_array[i] = (i + 1);
    }
}
