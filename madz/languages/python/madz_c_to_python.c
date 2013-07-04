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

//madz Python Pointer Type
static __madz_TYPE_pointer_object* new__madz_TYPE_pointer_object(PyObject *args){
	__madz_TYPE_pointer_object *self;
	self = PyObject_new(__madz_TYPE_pointer_object, &__madz_TYPE_pointer_object_Type);
	if (self == NULL){
		return NULL;
	}
	self->value = NULL;
	return self;
}
static void __madz_TYPE_pointer_object_dealloc(__madz_TYPE_pointer_object  *self){
	Py_XDECREF(self->value);
	PyObject_del(self);
}

static int __madz_TYPE_pointer_init(__madz_TYPE_pointer_object *self, PyObject *args, PyObject **kwargs){
	PyObject *value = NULL;

	PyObject *tmp;
	
	if(!PyArg_ParseTuple(args, "O", value){
			 return -1;
		}
	tmp = self->value;
	Py_INCREF(value);
	self->value = value;
	Py_XDECREF(tmp)
	return 0;
}

static PyMemberDef ___madz_TYPE_Point3d_object_members[] ={
	{"value", T_OBJECT_EX, offsetof(__madz_TYPE_pointer_object, value), 0, PyDoc_STR("Value Being Pointed To")},
	{NULL,NULL}}
	
___madz_TYPE_pointer_object_Type = {
    PyObject_HEAD_INIT(NULL)
    0, /*ob_size*/
    "madz.python.Pointer", /*tp_name*/
    sizeof(__madz_TYPE_pointer_object), /*tp_basicsize*/
    0, /*tp_itemsize*/
    (destructor)__madz_TYPE_pointer_object_dealloc, /*tp_dealloc*/
    0, /*tp_print*/
    0, /*tp_getattr*/
    0, /*tp_setattr*/
    0, /*tp_compare*/
    0, /*tp_repr*/
    0, /*tp_as_number*/
    0, /*tp_as_sequence*/
    0, /*tp_as_mapping*/
    0, /*tp_hash */
    0, /*tp_call*/
    0, /*tp_str*/
    0, /*tp_getattro*/
    0, /*tp_setattro*/
    0, /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    "Noddy objects", /* tp_doc */
    0,	/* tp_traverse */
    0,	/* tp_clear */
    0,	/* tp_richcompare */
    0,	/* tp_weaklistoffset */
    0,	/* tp_iter */
    0,	/* tp_iternext */
    0, /* tp_methods */
    ___madz_TYPE_Point3d_object_members, /* tp_members */
    0, /* tp_getset */
    0, /* tp_base */
    0, /* tp_dict */
    0, /* tp_descr_get */
    0, /* tp_descr_set */
    0, /* tp_dictoffset */
    (initproc)__madz_TYPE_pointer_init, /* tp_init */
    0, /* tp_alloc */
    new__madz_TYPE_pointer_object, /* tp_new */
};


