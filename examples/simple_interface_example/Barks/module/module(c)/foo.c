#include <stdio.h>

typedef struct{
	int x;
	int y;

}point2d;

void do_foo(int i){
	printf("%d\n",i);
}

void do_obj_foo(void * theFoo, int j){
	printf("ObjFoo:%d\n",j);
}

int set_foo(void * foo, int j){
	point2d *bar = (point2d *)foo;
	bar->x = j;
	printf("set Foo's X to:%d\n",bar->x);
}
