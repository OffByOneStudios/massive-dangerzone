#include "madz.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

MADZINIT {
	
}

int helper(void* var1, void* var2, size_t size, char *str) {
	if (var1 != var2) {
        printf("invalid value for %s", str);
        return 1;
    }
    else {
        return 0;
    }
}

MADZOUTFUNC_test {
	helper(&MADZ(c__set0).test0_i64,  &1, sizeof(int64_t),  "test0_i64");
    helper(MADZ(c__set0).test0_i32,  2,   "test0_i32");
    helper(MADZ(c__set0).test0_i16,  3,   "test0_i16");
    helper(MADZ(c__set0).test0_i8,   4,   "test0_i8");
    helper(MADZ(c__set0).test0_u64,  5,   "test0_u64");
    helper(MADZ(c__set0).test0_u32,  6,   "test0_u32");
    helper(MADZ(c__set0).test0_u16,  7,   "test0_u16");
    helper(MADZ(c__set0).test0_u8,   8,   "test0_u8");
    helper(MADZ(c__set0).test0_f64,  .1,  "test0_f64");
    helper(MADZ(c__set0).test0_f32,  .2,  "test0_f32");
    helper(MADZ(c__set0).test0_vp,   0,   "test0_vp");
    helper(MADZ(c__set0).test1_var,  0.0, "test1_var");
    
    MADZ(c__set0).test1_func();
    
    helper(MADZ(c__set0).test1_var,         16.0, "test1_var after running test1_func");
    helper(MADZ(c__set0).test2_func0(),     9,    "test2_func0");
    helper(MADZ(c__set0).test2_func1(2,3),  5,    "test2_func1");
    helper(MADZ(c__set0).test3_var0,        0.0,  "test3_var0");
    helper(MADZ(c__set0).test3_var1,        1.0,  "test3_var1");
    helper(MADZ(c__set0).test3_var_pointer, &(MADZ(c__set0).test3_var0), "test3_var_pointer");
    
    MADZ(c__set0).test3_func();
    
    helper(MADZ(c__set0).test3_var_pointer,     &(MADZ(c__set0).test3_var1), "test3_var_pointer after running test_3_func");
    helper(MADZ(c__set0).test4_var_simple,      1, "test4_var_simple");
    helper(MADZ(c__set0).test4_var_struct.var,  1, "test4_var_struct.var");
    helper(MADZ(c__set0).test4_var_struct.varp, &(MADZ(c__set0).test4_var_struct.var), "test4_var_simple");
    
    int i;
    
    for (i=1;i<=16;i++)
    {
        helper(MADZ(c__set0).test4_var_array[i-1], i, printf("test4_var_array[%d]", i));
    }
    
    
    int testa [32];
    
    for (i=0;i<32;i++) {
        testa[i] = i;
    }
    
    uint8_t testb = 1;
    MADZTYPE(c__set0, test5_struct) output;
    
    output = MADZ(c__set0).test5_func(testa, testb);
    size_t size = 32;
    
    if (memcmp(testa, output.a, size) != 0) {
        printf("invalid value for test5_struct.a");
    }
    
    helper(output.b, testb, "test5_struct.b");
}