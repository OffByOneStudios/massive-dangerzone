#include "header.h"

void test5_init()
{

}

MADZOUT::_t::test5_struct MADZOUT::_f::test5_func(int32_t a[32], uint8_t b) {
    MADZOUT::_t::test5_struct ret;
    ret.b = b;

    for (int i = 0; i < 32; i++) {
        ret.a[i] = a[i];
    }

    return ret;
}
