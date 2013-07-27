#include "header.h"

void test0_init()
{
    madz::cpp::set0::_.test0_i64 = 1;
    madz::cpp::set0::test0_i32 = 2;
    ::test0_i16 = 3;
    test0_i8 = 4;

    test0_u64 = 5;
    test0_u32 = 6;
    test0_u16 = 7;
    test0_u8 = 8;

    test0_f64 = .1;
    test0_f32 = .2;

    test0_vp = 0;
}
