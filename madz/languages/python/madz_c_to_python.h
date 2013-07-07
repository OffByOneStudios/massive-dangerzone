/*MADZ_c_to_pyobject.h
@OffbyOneStudios 2013
Helper functions for boxing MADZ c primitves into pyobject
*/
#include <inttypes.h>
#include "Python.h"

//Integers to Python
PyObject * MADZ_int8_to_pyobject(int8_t c);
PyObject * MADZ_int16_to_pyobject(int16_t c);
PyObject * MADZ_int32_to_pyobject(int32_t c);
PyObject * MADZ_int64_to_pyobject(int64_t c);

//Unsigned Integers to Python
PyObject * MADZ_uint8_to_pyobject(uint8_t c);
PyObject * MADZ_uint16_to_pyobject(uint16_t c);
PyObject * MADZ_uint32_to_pyobject(uint32_t c);
PyObject * MADZ_uint64_to_pyobject(uint64_t c);

//Python to Integers
int8_t MADZ_pyobject_to_int8(PyObject *p);
int16_t MADZ_pyobject_to_int16(PyObject *p);
int32_t MADZ_pyobject_to_int32(PyObject *p);
int64_t MADZ_pyobject_to_int64(PyObject *p);

//Python to Unsigned Integers
uint8_t MADZ_pyobject_to_uint8(PyObject *p);
uint16_t MADZ_pyobject_to_uint16(PyObject *p);
uint32_t MADZ_pyobject_to_uint32(PyObject *p);
uint64_t MADZ_pyobject_to_uint64(PyObject *p);

//Floating Point to Python
PyObject * MADZ_float_to_pyobject(float c);
PyObject * MADZ_double_to_pyobject(double c);

//Python to Floating Point
float MADZ_pyobject_to_float(PyObject *p);
double MADZ_pyobject_to_double(PyObject *p);

//Char to Python
PyObject * MADZ_char_to_pyobject(char c);
char MADZ_pyobject_to_char(PyObject *c);


typedef struct{
	PyObject *value;
}__madz_TYPE_pointer_object;
static PyTypeObject ___madz_TYPE_pointer_object_Type;


//TODO Pointer boxing and unboxing
PyObject * MADZ_int8_pointer_to_pyobject(int8_t *c);
PyObject * MADZ_int16_pointer_to_pyobject(int16_t *c);
PyObject * MADZ_int32_pointer_to_pyobject(int32_t *c);
PyObject * MADZ_int64_pointer_to_pyobject(int64_t *c);

PyObject * MADZ_uint8_pointer_to_pyobject(uint8_t *c);
PyObject * MADZ_uint16_pointer_to_pyobject(uint16_t *c);
PyObject * MADZ_uint32_pointer_to_pyobject(uint32_t *c);
PyObject * MADZ_uint64_pointer_to_pyobject(uint64_t *c);

//Python to Integers
int8_t* MADZ_pyobject_to_int8_pointer(PyObject *p);
int16_t* MADZ_pyobject_to_int16_pointer(PyObject *p);
int32_t* MADZ_pyobject_to_int32_pointer(PyObject *p);
int64_t* MADZ_pyobject_to_int64_pointer(PyObject *p);

//Python to Unsigned Integers
uint8_t* MADZ_pyobject_to_uint8_pointer(PyObject *p);
uint16_t* MADZ_pyobject_to_uint16_pointer(PyObject *p);
uint32_t* MADZ_pyobject_to_uint32_pointer(PyObject *p);
uint64_t* MADZ_pyobject_to_uint64_pointer(PyObject *p);

//Floating Point to Python
PyObject * MADZ_float_pointer__to_pyobject(float *c);
PyObject * MADZ_double_pointer_to_pyobject(double *c);

//Python to Floating Point
float* MADZ_pyobject_to_float_pointer(PyObject *p);
double* MADZ_pyobject_to_double_double(PyObject *p);

