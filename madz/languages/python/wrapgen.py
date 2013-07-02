"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""
import sys
from collections import namedtuple
# TODO(Any) Fix importing

import shared
import madz.pyMDL as pdl
from madz.dependency import Dependency

# Box dict elements into a named tuple so that one function can be used to construct conversions.
tmpnode = namedtuple('node', ['name', 'type'], verbose = False)

class PythonGenerator(object):
    """Class to Generate C wrapper for python plugins."""

    def __init__(self, dependencies, namespace, description):
        self.dependencies = dependencies
        self.namespace = namespace
        self.description = description

        self.madz_prefix ="MADZ_TYPE"

    def mangle_namespace(self):
        """C Namespace Mangling"""
        # TODO(Clark) actually mangle this namespace
        return self.namespace

    def python_to_c_for_node(self, node):
        if isinstance(node.type, pdl.TypeInt):
            if node.type.width == 8:
                return "MADZ_pyobject_to_int8("  + node.name + ");\n"
            elif node.type.width == 16:
                return "MADZ_pyobject_to_int16(" + node.name + ");\n"
            elif node.type.width == 32:
                return "MADZ_pyobject_to_int32(" + node.name + ");\n"
            elif node.type.width == 64:
                return "MADZ_pyobject_to_int64(" + node.name + ");\n"

        elif isinstance(node.type, pdl.TypeUInt):
            if node.type.width == 8:
                return "MADZ_pyobject_to_uint8(" + node.name + ");\n"
            elif node.type.width == 16:
                return "MADZ_pyobject_to_uint16(" + node.name + ");\n"
            elif node.type.width == 32:
                return "MADZ_pyobject_to_uint32(" + node.name + ");\n"
            elif node.type.width == 64:
                return "MADZ_pyobject_to_uint64(" + node.name + ");\n"

        elif isinstance(node.type, pdl.TypeFloat):
            if node.type.width == 32:
                return "MADZ_pyobject_to_float(" + node.name +");\n"
            elif node.type.width == 64:
                return "MADZ_pyobject_to_double(" + node.name +");\n"

        # TODO(Clark) Complex Types

    def c_to_python_for_node(self, node):
        if isinstance(node.type, pdl.TypeInt):
            if node.type.width == 8:
                return "MADZ_int8_to_pyobject("  + node.name + ");\n"
            elif node.type.width == 16:
                return "MADZ_int16_to_pyobject("  + node.name + ");\n"
            elif node.type.width == 32:
                return "MADZ_int32_to_pyobject("  + node.name + ");\n"
            elif node.type.width == 64:
                return "MADZ_int64_to_pyobject("  + node.name + ");\n"

        elif isinstance(node.type, pdl.TypeUInt):
            if node.type.width == 8:
                return "MADZ_uint8_to_pyobject("  + node.name + ");\n"
            elif node.type.width == 16:
                return "MADZ_uint16_to_pyobject("  + node.name + ");\n"
            elif node.type.width == 32:
                return "MADZ_uint32_to_pyobject("  + node.name + ");\n"
            elif node.type.width == 64:
                return "MADZ_uint64_to_pyobject("  + node.name + ");\n"

        elif isinstance(node.type, pdl.TypeFloat):
            if node.type.width == 32:
                return "MADZ_float_to_pyobject(" + node.name +");\n"
            elif node.type.width == 64:
                return "MADZ_double_to_pyobject(" + node.name +");\n"

    def make_pyobject(self, struct_node):
            """Construct a PyObject struct.
            This struct's members contain dummy PyObject variables for each member in struct.
            Additionally they contain a pointer to struct.
            """
            res = "typedef struct{\n"
            for key, val in struct_node.type.elements.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tPyObject *"+key+";\n"

            res +="\t" + struct_node.name + " *c_val;\n" # Pointer to hidden struct
            res+="}" + self.madz_prefix + "_"+struct_node.name + "_object;\n"
            return res

    def make_pyobject_type(self, struct_node):
            """Create Python Type for pyobject"""
            return "static PyTypeObject " + self.madz_prefix+"_"+struct_node.name+"_object_Type;\n"

    def make_pyobject_to_c(self, struct_node):
        """Unbox struct_node's underlying c value."""
        res = "static " + self.madz_prefix + "_" + struct_node.name + "_object* " + self.madz_prefix + "_" + struct_node.name + "_object_to_" + self.madz_prefix + "_" + struct_node.name
        res += "(" + self.madz_prefix + "_" + struct_node.name + "_object *val){\n"
        res += "\treturn val->c_val;\n"
        res += "}\n"

        return res
    def make_c_to_pyobject(self, struct_node):
        """Box c_struct into python struct"""
        res = "static " + self.madz_prefix + "_" + struct_node.name + "* " + self.madz_prefix + "_" + struct_node.name + "_to_" + self.madz_prefix + "_" + struct_node.name +"_object"
        res += "(" + self.madz_prefix + "_" + struct_node.name + " *c_val){\n"

        res += "\t" + self.madz_prefix + "_" + struct_node.name + "_object *p = new_" + self.madz_prefix + "_" + struct_node.name + "(NULL);\n"
        res += "\tp->c_val = c_val;\n"
        res += "\treturn p;\n"
        res += "}\n"

        return res

    def make_pyobject_new(self, struct_node):
            """Create Function to Perform Tp_alloc on the pyObject struct."""
            res = "static " + self.madz_prefix + "_" + struct_node.name + "_object* new_" + self.madz_prefix + "_" + struct_node.name + "(PyObject *args){\n" # Function header
            res += "\t" + self.madz_prefix + "_" + struct_node.name + "_object *self;\n"  # Pointer to object
            res += "\tself = PyObject_new(" + self.madz_prefix + "_" + struct_node.name + "_object, &" + self.madz_prefix + "_" + struct_node.name + "_object_Type);\n" # Allocate object
            # Failed Construction Check
            res += "\tif (self == NULL){\n"
            res += "\t\treturn NULL;\n"
            res += "\t}\n"
            for key, val in struct_node.type.elements.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tself->"+key+" = NULL;\n"
            # Return pointer
            res += "\tself->c_val = NULL;\n"
            res +=  "\treturn self;\n"
            res += "}\n"
            return res

    def make_pyobject_dealloc(self, struct_node):
            """Constructs dealloc code for PyObject"""
            res = "static void " + self.madz_prefix + "_" + struct_node.name + "_object_dealloc(" + self.madz_prefix + "_" + struct_node.name + "_object  *self){\n" # Function Header
            #Decrement Class Attribute Pointers
            for key, val in struct_node.type.elements.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tPy_XDECREF("+key+");\n"
            # Dealloc Self
            res += "\tPyObject_del(self);\n"
            res +="}\n"

            return res


    def make_pyobject_hidden_dealloc(self, struct_node):
            """Creates method on PyObject that can free the object's hidden struct pointer.

            This is used if you need to deallocate the incoming struct from madz from python.
            """
            res = "static void "+self.madz_prefix + "_" + struct_node.name +"_free(" + self.madz_prefix + "_" + struct_node.name +" *self, PyObject *args){\n"
            res += "\tfree(self->c_struct);\n"
            res += "}\n"

            return res

    def make_pyobject_init(self, struct_node):
        """Creates C description for the class's python constructor."""
        res = "static int " + self.madz_prefix + "_" + struct_node.name +"_init(" + self.madz_prefix + "_" + struct_node.name +"_object *self, PyObject *args, PyObject){\n"
        argcount = 0
        parsetuple = ""
        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                res +="\tPyObject *"+key+" = NULL;\n"
                parsetuple += key + ", "
                argcount+=1
        parsetuple = parsetuple[0:-2]
        res += "\tPyObject *tmp;\n"

        # If The C struct is empty allocate it and place *args in it
        res += "\tif self->c_val == NULL{\n"
        res += "\t\tself->res = malloc(sizeof( " + self.madz_prefix + "_" + struct_node.name + "));\n"

        res += "\t\tif(!PyArg_ParseTuple(args, \"" + "O"*argcount + "\", " + parsetuple +"){\n"
        res += "\t\t\t return -1;\n"
        res += "\t\t}\n"

        for key, val in struct_node.type.elements.items():
            res += "\t\tself->c_val->" + key + " = " + self.python_to_c_for_node(tmpnode(key, val))


        #Pointer Magic
        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                res += "\t\ttmp = self->" + key +";\n"
                res += "\t\tPy_INCREF(" + key +");\n"
                res += "\t\tself->" + key +" = " + key +";\n"
                res += "\t\tPy_XDECREF(tmp)\n"
        res += "\t}\n" # Close null cval

        res += "\treturn 0;\n" # already has a cstruct, use that instead
        res += "}\n"
        return res

    def make_pyobject_method_table(self, struct_node):
        """Initializes method table.

        The method table for a python object constructed from a C struct will contain at least a method to deallocate the underlying c struct.
        Additionally it will contain entries for the function pointers attached to the object. These fp's are actually wrapped elsewhere

        # TODO(clark) Function pointers will need a naming scheme and local code to wrap the content into python

        """
        docstring = "#TODO(MADZ) add documentation support"
        res = "static PyMethodDef " +  self.madz_prefix + "_" + struct_node.name + "_object_methods[] ={\n"
        res +="\t{\"MADZ_finalize\", (PyCFunction) "  + self.madz_prefix + "_" + struct_node.name + "_free, METH_VARARGS, PyDoc_STR(\"" + docstring + "\")},\n"
        res +="\t{NULL,	NULL} //Bad method lookup sentinel\n"
        res += "};\n"

        return res

    def make_pyobject_member_table(self, struct_node):
        docstring = "#TODO(MADZ) add documentation support"
        res = "static PyMemberDef" + self.madz_prefix + "_" + struct_node.name + "_object_members[] ={\n"

        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                res += "\t{\"" + key +"\", T_OBJECT_EX, offsetof(" + self.madz_prefix + "_" + struct_node.name + "_object" + "," + key +"), 0, " + docstring +"},\n"

        res +="\t{NULL}\n"

        res +="};\n"

        return res

    def make_pyobject_getattr(self, struct_node):
        """Wraps getattr calls to access the cstruct."""
        res = "static PyObject* " + self.madz_prefix + "_" + struct_node.name + "_object_getattr("+self.madz_prefix + "_" + struct_node.name + "_object, char *name){\n"
        if_marker = "if" # simpler loop

        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                res += "\t"+if_marker +"(strcmp(name, \"" + key + "\") == 0){\n"
                res += "\t\tPyObject *v =" + self.c_to_python_for_node(tmpnode("self->c_val->"+key,val))
                res += "\t\tif(v == NULL){\n"
                res += "\t\t\tPy_INCREF(v);\n"
                res += "\t\t\treturn v;\n"
                res =="\t\t}\n"
                res +="\t}\n"
                if_marker= "else if"
        res +="\telse{\n"
        res +="\t\treturn Py_FindMethod(" +self.madz_prefix + "_" + struct_node.name + "_object_methods, (PyObject *)self, name);\n"
        res +="\t}\n"
        res +="}\n"

        return res

    def make_pyobject_setattr(self, struct_node):
        res = "static PyObject* " + self.madz_prefix + "_" + struct_node.name + "_object_setattr("+self.madz_prefix + "_" + struct_node.name + "_object, char *name, PyObject *v){\n"
        if_marker = "if" # simpler loop
        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                res += "\t"+if_marker +"(strcmp(name, \"" + key + "\") == 0){\n"
                res += "\t\tself->c_val->"+key + " = " + self.python_to_c_for_node(tmpnode("v", val))
                res += "\t\treturn 0l\n"
                res += "\t}\n"
                if_marker= "else if"
        res += "\treturn -1;\n"
        res += "}\n"
        return res

    def make_pyobject_type_table(self, struct_node):
        """Fill in PyTypeObject table."""
        res = "PyTypeObject " +self.madz_prefix + "_" + struct_node.name + "_" + "_Type = {\n"
        code_fragments = {
        "module_name":self.namespace+"."+struct_node.name,
        "object_type":self.madz_prefix + "_" + struct_node.name + "_object",
        "fn_dealloc":self.madz_prefix + "_" + struct_node.name + "_object_dealloc",
        "fn_getattr":self.madz_prefix + "_" + struct_node.name + "_object_getattr",
        "fn_setattr":self.madz_prefix + "_" + struct_node.name + "_object_setattr",
        "docstring":"# TODO(MADZ) Add DocString Support",
        "method_table":self.madz_prefix + "_" + struct_node.name + "_object_methods",
        "member_table":self.madz_prefix + "_" + struct_node.name + "_object__members",
        "fn_init":self.madz_prefix + "_" + struct_node.name + "object_init",
        "fn_new":"new_" + self.madz_prefix + "_" + struct_node.name
        }

        res += \
"""
    PyObject_HEAD_INIT(NULL)
    0, /*ob_size*/
    "{module_name}", /*tp_name*/
    sizeof({object_type}), /*tp_basicsize*/
    0, /*tp_itemsize*/
    (destructor){fn_dealloc}, /*tp_dealloc*/
    0, /*tp_print*/
    {fn_getattr}, /*tp_getattr*/
    {fn_setattr}, /*tp_setattr*/
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
    "{docstring}", /* tp_doc */
    0,	/* tp_traverse */
    0,	/* tp_clear */
    0,	/* tp_richcompare */
    0,	/* tp_weaklistoffset */
    0,	/* tp_iter */
    0,	/* tp_iternext */
    {method_table}, /* tp_methods */
    {member_table}, /* tp_members */
    0, /* tp_getset */
    0, /* tp_base */
    0, /* tp_dict */
    0, /* tp_descr_get */
    0, /* tp_descr_set */
    0, /* tp_dictoffset */
    (initproc){fn_init}, /* tp_init */
    0, /* tp_alloc */
    {fn_new}, /* tp_new */

""".format(**code_fragments)
        res +="};\n"
        return res

class WrapperGenerator(object):
    lang = shared.LanguageShared
    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub
        self._s_dir = self.plugin_stub.abs_directory
        self._b_dir = self.lang.get_build_directory(self.plugin_stub)
        self._w_dir = self.lang.get_wrap_directory(self.plugin_stub)
        self._o_dir = self.lang.get_output_directory(self.plugin_stub)

    def prep(self):
        if not (os.path.exists(self._w_dir)):
            os.makedirs(self._w_dir)

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        pass

    def generate(self):
        #Write shit here.
        gen = PythonGenerator([], self.plugin_stub.id.namespace, self.plugin_stub.description)
        # TODO(Clark) Implementation Order:
        # Get Pyobject, alloc and deallocing working
        # Get conversion functions generating

        c_glue = ""
        for node in gen.description.declarations():
            if isinstance(node.type, pdl.TypeStruct):
                c_glue += gen.make_pyobject(node)
                c_glue += gen.make_pyobject_type(node)
                c_glue += gen.make_pyobject_new(node)
                c_glue += gen.make_pyobject_dealloc(node)
                c_glue += gen.make_pyobject_hidden_dealloc(node)
                c_glue += gen.make_pyobject_to_c(node)
                c_glue += gen.make_c_to_pyobject(node)
                c_glue += gen.make_pyobject_init(node)
                c_glue += gen.make_pyobject_method_table(node)
                c_glue += gen.make_pyobject_member_table(node)
                c_glue += gen.make_pyobject_getattr(node)
                c_glue += gen.make_pyobject_setattr(node)
                c_glue += gen.make_pyobject_type_table(node)

        print c_glue
        print "\n\n\n\n"
        sys.exit(0)
