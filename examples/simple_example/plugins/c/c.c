#include "madz.h"

#include "stdio.h"

MADZINIT {
    printf("INIT C!\n");
}

MADZOUTFUNC_origin_distance {
	return MADZ(b).origin_distance((MADZTYPE(a,Point2d)) { .x = x, .y = y });
}
