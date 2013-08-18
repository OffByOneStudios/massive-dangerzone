/* This header provides the macros for using madz in c */
#include "madz.h"

/* For printf */
#include <stdio.h>

/* For math functions. This requires the math library as specified in the plugin description */
#include <math.h>

MADZINIT {
	MADZOUT_a_global = 1;
}

MADZOUTFUNC_print_global {
	printf("The value of a_global is %d", MADZOUT_a_global);
}

MADZOUTFUNC_do_math_on_global {
	return powf((float)MADZOUT_a_global, 1.5);
}