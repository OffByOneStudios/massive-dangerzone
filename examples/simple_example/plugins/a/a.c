#include "madz.h"

#define MADZTHIS(object){}
#define MADZTHISTYPE(object)

float MADZTHIS(distance)(MADZTHISTYPE(Point2d) a, MADZTHISTYPE(Point2d) b){
	return (a.x-b.x) + (a.y - b.y);
}