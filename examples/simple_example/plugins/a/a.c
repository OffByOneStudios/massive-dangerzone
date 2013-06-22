#include "madz.h"

#include "math.h"

MADZOUT_a_var = 13;

MADZOUT_origin = (MADZTYPE(MADZTHIS,Point2d)) { .x = 0.0, .y = 0.0 };

MADZOUT_distance{
    xs = (a.x - b.x);
    xs = xs * xs;

    ys = (a.y - b.y);
    ys = ys * ys;
	return sqrtf(xs + ys);
}
