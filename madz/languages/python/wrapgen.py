"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""
import sys
# TODO(Clark) Implementation Order:
# Get Pyobject, alloc and deallocing working
# Get conversion functions generating

# TODO(Any) Fix importing

import shared
import madz.pyMDL as pdl
from madz.dependency import Dependency

class PythonGenerator(object):
    """Class to Generate C wrapper for python plugins."""

    def __init__(self, dependencies, namespace, description):
        self.dependencies = dependencies
        self.namespace = namespace
        self.declarations = description.declarations
        self.variables = description.variables
        self.madz_prefix ="MADZ_TYPE"

    def mangle_namespace(self):
        """C Namespace Mangling"""


        # TODO(Clark) actually mangle this namespace
        return self.namespace

    def get_visible_types(self):
        """Aggregates all types visible by this plugin."""
        res = []
        for dep in self.dependencies + [self]:
            for key, val in dep.declarations.items():
                pass

    def make_madz_c_header(self):
        """Returns String of C Header Component."""
        pass

    def make_type_conversions(self):
        pass

    def python_wrapper_from_struct(self, struct):
        """Generates Python Glue for accessing structs"""

        def py_parse_string_from_struct(name , struct):
            """Returns a parse format for a struct."""
            res = ""
            for key, val in struct.description.items():
                # Currently just boxes things into py_object
                if isinstance(val, pdl.TypeInt):
                    if val.width == 8 : res += "c" # THIS MIGHT BE A TYPO IN PYDOC http://docs.python.org/dev/c-api/arg.html#PyArg_ParseTuple
                    elif val.width == 16: res +="h"
                    elif val.width == 32: res +="i"
                    elif val.width == 64: res +="L"

                elif isinstance(val, pdl.TypeUInt):
                    if val.width == 8 : res += "B" # THIS MIGHT BE A TYPO IN PYDOC http://docs.python.org/dev/c-api/arg.html#PyArg_ParseTuple
                    elif val.width == 16: res +="H"
                    elif val.width == 32: res +="I"
                    elif val.width == 64: res +="K"

                elif isinstance(val, pdl.TypeFloat):
                    if val.width == 32: res +="f"
                    elif val.width == 64: res +="d"

                elif isinstance(val, pdl.TypePointer):
                    res += "O"

                elif isinstance(val, pdl.TypeArray):
                    raise NotImplementedError

                elif isinstance(val, pdl.NamedType):
                    res +="O"
            return res


        def make_pyobject(name, struct):
            """Construct a PyObject struct.
            This struct's members contain dummy PyObject variables for each member in struct.
            Additionally they contain a pointer to struct.
            """
            res = "typedef struct{\n"
            for key, val in struct.description.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tPyObject *"+key+";\n"

            res +="\t"+name+" *c_val;\n" # Pointer to hidden struct
            res+="}"+self.madz_prefix+"_"+name+"_object;\n"
            return res

        def make_pyobject_type(name, struct):
            """Create Python Type for pyobject"""
            return "static PyTypeObject " + self.madz_prefix+"_"+name+"_object_Type;\n"

        def make_new(name, struct):
            """Create Function to Perform Tp_alloc on the pyObject struct."""
            res = "static " + self.madz_prefix + "_" + name + "_object new_" + self.madz_prefix + "_" + name + "(PyObject *args){" # Function header
            res += "\t" + self.madz_prefix + "_" + name + "_object *self;"  # Pointer to object

            res += "\tself = PyObject_new(" + self.madz_prefix + "_" + name + "_object, &" + self.madz_prefix + "_" + name + "_object_Type);\n" # Allocate object

            # Failed Construction Check
            res += "\tif (self == NULL){\n"
            res += "\t\treturn NULL;\n"
            res += "\t}\n"

            # Initialize pointers to null

            for key, val in struct.description.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tself->"+key+" = NULL;\n"
            # Return pointer

            res += "\treturn self;"
            res +="}\n"
            return res

        def make_dealloc(name, struct):
            """Constructs dealloc code for PyObject"""
            res = "static void " + self.madz_prefix + "_" + name + "_object_dealloc(" + self.madz_prefix + "_" + name + "_object  *self){\n" # Function Header
            #Decrement Class Attribute Pointers
            for key, val in struct.description.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tPy_XDECREF("+key+");\n"
            # Dealloc Self
            res += "\tPyObject_del(self);"

            return res


        def make_init(name, struct):
            """Creates C description for the class's python constructor."""
            res = "static int " + self.madz_prefix + "_" + name +"_init(" + self.madz_prefix + "_" + name +"_object *self, PyObject *args, PyObject){\n" # Header

            # Declare Pointers for internal state
            for key, val in struct.description.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tPyObject *"+key+" = NULL;\n"

            res += "\tPyObject *tmp;\n"
            # Allocate space for c struct
            res += "\tif self->c_val == NULL{\n"
            res += "\t\tself->res=malloc(sizeof( " + self.madz_prefix + "_" + name + "));\n"
            res += "\t}\n"

            parse_call = py_parse_string_from_struct(name, struct)
            res +="\tif(!PyArg_ParseTuple(args, \""

            for key,val in struct.description.items():
                if not isinstance(val,pdl.TypeFunction):
                    res+="O"
            res +="\", "
            for key, val in struct.declarations.items():
                if not isinstance(val,pdl.TypeFunction):
                    res+="&" + key +", "
            res += res[0:len(res)-2] + ")){\n"
            res += "\t\treturn -1;\n"
            res += "}\n"

            # TODO(Clark) Unbox pyobject attributes into c_struct


        def make_hidden_dealloc(name, struct):
            """Creates method on PyObject that can free the object's hidden struct pointer.

            This is used if you need to deallocate the incoming struct from madz from python.
            """
            res = "static void "+self.madz_prefix + "_" + name +"_free(" + self.madz_prefix + "_" + name +" *self, PyObject *args){\n"
            res += "\tfree(self->c_struct);\n"
            res += "}\n"

            return res

        def make_method_table(name, struct):
            """Creates a method table for the PyObject.
            This will only include the hidden dealloc method in the case of regular structs.
            This will also contain methods that wrap function pointers attached to dependant modules.
            """
            # TODO(Clark) Methods attached to class need to be attached here.
            res = "PyMethodDef " + self.madz_prefix + "_" + name +"_object "+  self.madz_prefix + "_" + name +"_methods[] = {\n"
            res += "\tMADZ_free,	(PyCFunction)" + self.madz_prefix + "_" + name +"_free, METH_VARARGS, PyDoc_STR(\"You should Do Doc Forwarding\")},"
            res += "\t{NULL,	NULL}\n"
            res += "};\n"

            return res

        def make_attr_functions(name, struct):
            """Creates custom getattr/setattr methods for object.

            These methods intercept class property read/writes and redirects them to the hidden struct.

            """
            pass

        def make_python_type_array(name, struct):
            """Fills in PyTypeObject array with the above functions."""
            pass

        def wrap_struct_function_pointers(name, struct):
            """wraps any function pointers associated with struct (like when a plugin is included as a dependency)
            and creates PyObjects from their results.
            """

        pass
    def make_plugin_functions(self):
        """Creates functions associated with the actual functions described in the interface.
        These box incomming types into python, call the python function associated with the module, and unbox results.
        """
        pass

    def make_module_init(self):
        """Creates function to bind a python module to this interface description.

        This module must contain matching names for the functions described in the plugin description
        """
        pass


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

    def generate():
        pass