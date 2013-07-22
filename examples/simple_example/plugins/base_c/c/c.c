#include "madz.h"

#include "stdio.h"

MADZINIT {
    printf("INIT C!\n");
}

MADZOUTFUNC_origin_distance {
	MADZTYPE(base_c__a,Point2d) ret;
	ret.x = x;
	ret.y = y;
	return MADZ(base_c__b).origin_distance(ret);
}
