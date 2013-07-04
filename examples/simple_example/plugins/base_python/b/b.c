#include "madz.h"

#include "stdio.h"

MADZINIT {
    MADZOUT_origin = (MADZTYPE(base_c__a,Point2d)) { .x = 0.0, .y = 0.0 };

    printf("INIT B!\n");    
}


MADZOUTFUNC_origin_distance {
	return MADZ(base_c__a).distance(a, MADZOUT_origin);
}
