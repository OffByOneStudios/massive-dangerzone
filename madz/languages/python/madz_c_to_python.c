/*MADZ_c_to_pyobject.c
@OffbyOneStudios 2013
Helper functions for boxing MADZ c primitves int32o pyobject
*/
#include "madz_c_to_python.h"
//Integers to Python
PyObject * MADZ_int8_to_pyobject(int8_t c)
{
	return PyLong_FromLong((long)c);
}

PyObject * MADZ_int16_to_pyobject(int16_t c)
{
	return PyLong_FromLong((long)c);
}

PyObject * MADZ_int32_to_pyobject(int32_t c)
{
	return PyLong_FromLong((long)c);
}

PyObject * MADZ_int64_to_pyobject(int64_t c)
{
	return PyLong_FromLongLong((long long)c);
}


//Unsigned Integers to Python
PyObject * MADZ_uint8_to_pyobject(uint8_t c)
{
	return PyLong_FromUnsignedLong( (unsigned long) c);
}

PyObject * MADZ_uint16_to_pyobject(uint16_t c)
{
	return PyLong_FromUnsignedLong( (unsigned long) c);
}

PyObject * MADZ_uint32_to_pyobject(uint32_t c)
{
	return PyLong_FromUnsignedLong( (unsigned long) c);
}

PyObject * MADZ_uint64_to_pyobject(uint64_t c)
{
	return PyLong_FromUnsignedLongLong( (unsigned long long) c);
}

//Python to Integers
int8_t MADZ_pyobject_to_int8(PyObject *p)
{
	return (int8_t)PyLong_AsLong(p);
}

int16_t MADZ_pyobject_to_int16(PyObject *p)
{
	return (int16_t)PyLong_AsLong(p);
}

int32_t MADZ_pyobject_to_int32(PyObject *p)
{
	return (int32_t)PyLong_AsLong(p);
}

int64_t MADZ_pyobject_to_int64(PyObject *p)
{
	return (int64_t)PyLong_AsLongLong(p);
}


//Python to Unsigned Integers
uint8_t MADZ_pyobject_to_uint8(PyObject *p)
{
	return (uint8_t)PyLong_AsUnsignedLong(p);
}

uint16_t MADZ_pyobject_to_uint16(PyObject *p)
{
	return (uint8_t)PyLong_AsUnsignedLong(p);
}

uint32_t MADZ_pyobject_to_uint32(PyObject *p)
{
	return (uint8_t)PyLong_AsUnsignedLong(p);
}

uint64_t MADZ_pyobject_to_uint64(PyObject *p)
{
	return (uint8_t)PyLong_AsUnsignedLongLong(p);
}


//Floating Point to Python
PyObject * MADZ_float_to_pyobject(float c)
{
	return PyFloat_FromDouble( (double) c);
}

PyObject * MADZ_double_to_pyobject(double c)
{
	return PyFloat_FromDouble(c);
}


//Python to Floating Point
float MADZ_pyobject_to_float(PyObject *p)
{
	return (float)PyFloat_AsDouble(p);
}

double MADZ_pyobject_to_double(PyObject *p)
{
	return PyFloat_AsDouble(p);
}

//Char to Python
PyObject * MADZ_char_to_pyobject(char c)
{
	return PyUnicode_FromStringAndSize(&c,1);
}

char MADZ_pyobject_to_char(PyObject *c)
{
	return *PyUnicode_AsUTF8(c);
}


//TODO Pointer boxing and unboxing
PyObject * MADZ_int8_pointer_to_pyobject(int8_t *c){
    return PyCapsule_New((void *)c, "int8");
}

PyObject * MADZ_int16_pointer_to_pyobject(int16_t *c){
    return PyCapsule_New((void *)c, "int16");
}

PyObject * MADZ_int32_pointer_to_pyobject(int32_t *c){
    return PyCapsule_New((void *)c, "int32");
}

PyObject * MADZ_int64_pointer_to_pyobject(int64_t *c){
    return PyCapsule_New((void *)c, "int64");
}

PyObject * MADZ_uint8_pointer_to_pyobject(uint8_t *c){
    return PyCapsule_New((void *)c, "uint8");
}

PyObject * MADZ_uint16_pointer_to_pyobject(uint16_t *c){
    return PyCapsule_New((void *)c, "uint16");
}

PyObject * MADZ_uint32_pointer_to_pyobject(uint32_t *c){

    return PyCapsule_New((void *)c, "uint32");
}

PyObject * MADZ_uint64_pointer_to_pyobject(uint64_t *c){
    return PyCapsule_New((void *)c, "uint64");
}

int8_t* MADZ_pyobject_to_int8_pointer(PyObject *p){
    return (int8_t*)PyCapsule_GetPointer(p, "int8");
}
int16_t* MADZ_pyobject_to_int16_pointer(PyObject *p){
    return (int16_t*)PyCapsule_GetPointer(p, "int16");
}

int32_t* MADZ_pyobject_to_int32_pointer(PyObject *p){
     return (int32_t*)PyCapsule_GetPointer(p, "int32");
}
int64_t* MADZ_pyobject_to_int64_pointer(PyObject *p){
     return (int64_t*)PyCapsule_GetPointer(p, "int64");
}

//Python to Unsigned Integers
uint8_t* MADZ_pyobject_to_uint8_pointer(PyObject *p){
     return (uint8_t*)PyCapsule_GetPointer(p, "uint8");
}

uint16_t* MADZ_pyobject_to_uint16_pointer(PyObject *p){
    return (uint16_t*)PyCapsule_GetPointer(p, "uint16");
}

uint32_t* MADZ_pyobject_to_uint32_pointer(PyObject *p){
    return (uint32_t*)PyCapsule_GetPointer(p, "uint32");
}

uint64_t* MADZ_pyobject_to_uint64_pointer(PyObject *p){
    return (uint64_t*)PyCapsule_GetPointer(p, "uint64");
}

//Floating Point to Python
PyObject * MADZ_float_pointer__to_pyobject(float *c){
    return PyCapsule_New((void*) c, "float");
}
PyObject * MADZ_double_pointer_to_pyobject(double *c){
    return PyCapsule_New((void*) c, "double");
}

//Python to Floating Point
float *MADZ_pyobject_to_float_pointer(PyObject *p){
    return (float*)PyCapsule_GetPointer(p, "float");
}

double *MADZ_pyobject_to_double_double(PyObject *p){
    return (double*)PyCapsule_GetPointer(p, "double");
}