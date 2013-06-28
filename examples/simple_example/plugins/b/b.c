#include "madz.h"

#include "stdio.h"

MADZINIT {
    MADZOUT_origin = (MADZTYPE(a,Point2d)) { .x = 0.0, .y = 0.0 };

    printf("INIT B!\n");    
}


MADZOUTFUNC_origin_distance {
	return MADZ(a).distance(a, MADZOUT_origin);
}
