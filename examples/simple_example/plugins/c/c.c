#include "madz.h"

MADZINIT {}

MADZOUTFUNC_origin_distance {
	return MADZ(b).origin_distance((MADZTYPE(a,Point2d)) { .x = x, .y = y });
}
