#include "header.h"

void test4_init()
{
    test4_var_simple = 1;

    test4_var_struct.var = 1;
    test4_var_struct.varp = &(test4_var_struct.var);

    for (int i = 0; i < 16; i++) {
        test4_var_array[i] = (i + 1);
    }
}
