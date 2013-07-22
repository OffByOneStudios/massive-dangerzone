#include "madz.h"

#include "math.h"
#include "stdio.h"

MADZINIT {
    MADZOUT_a_var = 13;
    MADZOUT_a_uvar = 13;

    MADZOUT_origin.x=0.0;
	MADZOUT_origin.y=0.0;

    printf("INIT A!\n");
}

MADZOUTFUNC_distance {
	float ys = (a.y - b.y);
    float xs = (a.x - b.x);
	
    xs = xs * xs;
    ys = ys * ys;

	return sqrtf(xs + ys);
}
