#include "madz.h"

#include "math.h"

MADZINIT{
    MADZOUT_a_var = 13;

    MADZOUT_origin = (MADZTYPE(,Point2d)) { .x = 0.0, .y = 0.0 };
}

MADZOUTFUNC_distance{
    float xs = (a.x - b.x);
    xs = xs * xs;

    float ys = (a.y - b.y);
    ys = ys * ys;
	return sqrtf(xs + ys);
}
