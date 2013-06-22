#include "madz.h"

MADZOUT_origin = (MADZTYPE(a,Point2d)) { .x = 0.0, .y = 0.0 };

MADZOUT_origin_distance{
	return MADZ(a,distance)(a, origin);
}
