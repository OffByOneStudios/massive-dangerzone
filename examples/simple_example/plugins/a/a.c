#include "madz.h"

#include "math.h"
#include "stdio.h"

MADZINIT{
    MADZOUT_a_var = 13;

    MADZOUT_origin = (MADZTYPE(,Point2d)) { .x = 0.0, .y = 0.0 };

    printf("TEST!\n");
}

MADZOUTFUNC_distance{
    float xs = (a.x - b.x);
    xs = xs * xs;

    float ys = (a.y - b.y);
    ys = ys * ys;
	return sqrtf(xs + ys);
}
