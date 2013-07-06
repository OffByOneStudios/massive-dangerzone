"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""
import sys,os
from collections import namedtuple
from ..c import wrapgen as c_wrapgen
# TODO(Any) Fix importing

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
        self.mangled_namespace = self._namespace_mangle(namespace)
        self.type_prefix = "___madz_TYPE"
        self._gen_table = c_wrapgen.CGenerator._gen_table

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

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

        elif isinstance(node.type, pdl.NamedType):
            return self.type_prefix + "_" + node.type.symbol + "_object_to_" + self.type_prefix + node.type.symbol +"(" + node.name +");\n"

        # TODO(Clark) Complex Types
        elif isinstance(node.type, pdl.TypePointer):
            ctype = self._gen_table[node.type.type.node_type()](self, node.type.type, "")
            return "(" + ctype + ")PyCapsule_GetPointer(" + node.name +",\" " + ctype + "\");\n"


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

        elif isinstance(node.type, pdl.NamedType):
            return self.type_prefix + "_" + node.type.symbol + "_to_" + self.type_prefix + "_" + node.type.symbol +"_object(" + node.name + ");\n"


        elif isinstance(node.type, pdl.TypePointer):
            ctype = self._gen_table[node.type.type.node_type()](self, node.type.type, "")
            return "PyCapsule_New((void *)" + node.name + ", \""+ctype +"\", NULL);\n"

        else:
            raise NotImplementedError(node.name)
    def make_pyobject(self, struct_node):
            """Construct a PyObject struct."""
            res = "typedef struct{\n"
            for key, val in struct_node.type.elements.items():
                if not isinstance(val, pdl.TypeFunction):
                    res +="\tPyObject *"+key+";\n"

            res +="\t" + struct_node.name + " c_val;\n" # Pointer to hidden struct
            res+="}" + self.type_prefix + "_"+struct_node.name + "_object;\n"
            return res

    def make_pyobject_type(self, struct_node):
            """Create Python Type for pyobject"""
            return "static PyTypeObject " + self.type_prefix+"_"+struct_node.name+"_object_Type;\n"

    def make_pyobject_to_c(self, struct_node):
        """Unbox struct_node's underlying c value."""
        res = "static " + self.type_prefix + "_" + struct_node.name + "_object* " + self.type_prefix + "_" + struct_node.name + "_object_to_" + self.type_prefix + "_" + struct_node.name
        res += "(" + self.type_prefix + "_" + struct_node.name + "_object *val){\n"
        res += "\treturn val.c_val;\n"
        res += "}\n"

        return res

    def make_c_to_pyobject(self, struct_node):
        """Box c_struct into python struct"""
        res = "static " + self.type_prefix + "_" + struct_node.name + "* " + self.type_prefix + "_" + struct_node.name + "_to_" + self.type_prefix + "_" + struct_node.name +"_object"
        res += "(" + self.type_prefix + "_" + struct_node.name + " *c_val){\n"

        res += "\t" + self.type_prefix + "_" + struct_node.name + "_object *p = new_" + self.type_prefix + "_" + struct_node.name + "(NULL);\n"
        res += "\tp.c_val = c_val;\n"
        res += "\treturn p;\n"
        res += "}\n"

        return res

    def make_pyobject_new(self, struct_node):
            """Create Function to Perform Tp_alloc on the pyObject struct."""
            res = "static " + self.type_prefix + "_" + struct_node.name + "_object* new_" + self.type_prefix + "_" + struct_node.name + "(PyObject *args){\n" # Function header
            res += "\t" + self.type_prefix + "_" + struct_node.name + "_object *self;\n"  # Pointer to object
            res += "\tself = PyObject_new(" + self.type_prefix + "_" + struct_node.name + "_object, &" + self.type_prefix + "_" + struct_node.name + "_object_Type);\n" # Allocate object
            # Failed Construction Check
            res += "\tif (self == NULL){\n"
            res += "\t\treturn NULL;\n"
            res += "\t}\n"

            # Return pointer

            res +=  "\treturn self;\n"
            res += "}\n"
            return res

    def make_pyobject_dealloc(self, struct_node):
            """Constructs dealloc code for PyObject"""
            res = "static void " + self.type_prefix + "_" + struct_node.name + "_object_dealloc(" + self.type_prefix + "_" + struct_node.name + "_object  *self){\n" # Function Header
            #Decrement Class Attribute Pointers

            # Dealloc Self
            res += "\tPyObject_del(self);\n"
            res +="}\n"

            return res


    def make_pyobject_hidden_dealloc(self, struct_node):
            """Creates method on PyObject that can free the object's hidden struct pointer.

            This is used if you need to deallocate the incoming struct from madz from python.
            """
            res = "static void "+self.type_prefix + "_" + struct_node.name +"_free(" + self.type_prefix + "_" + struct_node.name +" *self, PyObject *args){\n"
            res += "\tfree(self.c_struct);\n"
            res += "}\n"

            return res

    def make_pyobject_init(self, struct_node):
        """Creates C description for the class's python constructor."""
        res = "static int " + self.type_prefix + "_" + struct_node.name +"_init(" + self.type_prefix + "_" + struct_node.name +"_object *self, PyObject *args, PyObject **kwargs){\n"
        argcount = 0
        parsetuple = ""
        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                res +="\tPyObject *p"+key+" = NULL;\n"
                parsetuple += "p" + key + ", "
                argcount+=1
        parsetuple = parsetuple[0:-2]
        res += "\tPyObject *tmp;\n"

        # If The C struct is empty allocate it and place *args in it
        res += "\tif self->c_val == NULL{\n"
        res += "\t\tself->res = malloc(sizeof( " + self.type_prefix + "_" + struct_node.name + "));\n"

        res += "\t\tif(!PyArg_ParseTuple(args, \"" + "O"*argcount + "\", " + parsetuple +"){\n"
        res += "\t\t\t return -1;\n"
        res += "\t\t}\n"

        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                if isinstance(val, pdl.TypePointer):
                    res += "\t\tself.c_val->" + key + " = " + self.python_to_c_for_node(tmpnode(key, val))
                else:
                    res += "\t\tself.c_val." + key + " = " + self.python_to_c_for_node(tmpnode(key, val))

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

        res = "static PyMethodDef " +  self.type_prefix + "_" + struct_node.name + "_object_methods[] ={\n"
        res +="\t{\"MADZ_finalize\", (PyCFunction) "  + self.type_prefix + "_" + struct_node.name + "_free, METH_VARARGS, PyDoc_STR(\"" + struct_node.doc + "\")},\n"
        res +="\t{NULL,	NULL} //Bad method lookup sentinel\n"
        res += "};\n"

        return res

    def make_pyobject_member_table(self, struct_node):
        def member_macro_for_type(t):
            if isinstance(t,pdl.TypeInt):
                if t.width == 8:
                    return "T_BYTE"
                elif t.width == 16:
                    return "T_SHORT"
                elif t.width == 32:
                    return "T_INT"
                elif t.width == 64:
                    return "T_LONGLONG"
            elif isinstance(t, pdl.TypeUInt):
                if t.width == 8:
                    return "T_BYTE"
                elif t.width == 16:
                    return "T_SHORT"
                elif t.width == 32:
                    return "T_INT"
                elif t.width == 64:
                    return "T_LONGLONG"

            elif isinstance(t, pdl.TypeFloat):
                if t.width == 32:
                    return "T_FLOAT"
                else:
                    return "T_DOUBLE"
            else:
                return "T_OBJECT_EX"


        docstring = "#TODO(MADZ) add documentation support"
        res = "static PyMemberDef" + self.type_prefix + "_" + struct_node.name + "_object_members[] ={\n"

        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                if isinstance(val,pdl.TypePointer):
                    res += "\t{\"" + key +"\", T_OBJECT_EX, offsetof(" + self.type_prefix + "_" + struct_node.name + "_object" + "," + key +"), 0, PyDoc_STR(\"" + struct_node.doc + "\")},\n"
                else:
                    res += "\t{\"" + key +"\", " +member_macro_for_type(val) + ", offsetof(" + self.type_prefix + "_" + struct_node.name + "_object" + "," + key +"), 0, PyDoc_STR(\"" + struct_node.doc + "\")},\n"
        res +="\t{NULL}\n"

        res +="};\n"

        return res

    def make_pyobject_getattr(self, struct_node):
        """Wraps getattr calls to access the cstruct"""
        res = "static PyObject* " + self.type_prefix + "_" + struct_node.name + "_object_getattr("+self.type_prefix + "_" + struct_node.name + "_object, char *name){\n"
        if_marker = "if" # simpler loop

        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                if isinstance(val, pdl.TypePointer):
                    res += "\t"+if_marker +"(strcmp(name, \"" + key + "\") == 0){\n"
                    res += "\t\tPyObject *v =" + self.c_to_python_for_node(tmpnode("self.c_val->"+key,val))
                    res += "\t\tif(v == NULL){\n"
                    res += "\t\t\tPy_INCREF(v);\n"
                    res += "\t\t\treturn v;\n"
                    res =="\t\t}\n"
                    res +="\t}\n"
                else:
                    res += "\t"+if_marker +"(strcmp(name, \"" + key + "\") == 0){\n"
                    res += "\t\tPyObject *v =" + self.c_to_python_for_node(tmpnode("self.c_val."+key,val))
                    res += "\t\tif(v == NULL){\n"
                    res += "\t\t\tPy_INCREF(v);\n"
                    res += "\t\t\treturn v;\n"
                    res =="\t\t}\n"
                    res +="\t}\n"
                if_marker= "else if"
        res +="\telse{\n"
        res +="\t\treturn Py_FindMethod(" +self.type_prefix + "_" + struct_node.name + "_object_methods, (PyObject *)self, name);\n"
        res +="\t}\n"
        res +="}\n"

        return res

    def make_pyobject_setattr(self, struct_node):
        res = "static PyObject* " + self.type_prefix + "_" + struct_node.name + "_object_setattr("+self.type_prefix + "_" + struct_node.name + "_object, char *name, PyObject *v){\n"
        if_marker = "if" # simpler loop
        for key, val in struct_node.type.elements.items():
            if not isinstance(val, pdl.TypeFunction):
                if isinstance(val, pdl.TypePointer):
                    res += "\t"+if_marker +"(strcmp(name, \"" + key + "\") == 0){\n"
                    res += "\t\tself.c_val->"+key + " = " + self.python_to_c_for_node(tmpnode("v", val))
                    res += "\t\treturn 0l\n"
                    res += "\t}\n"
                else:
                    res += "\t"+if_marker +"(strcmp(name, \"" + key + "\") == 0){\n"
                    res += "\t\tself.c_val."+key + " = " + self.python_to_c_for_node(tmpnode("v", val))
                    res += "\t\treturn 0l\n"
                    res += "\t}\n"
                if_marker= "else if"
        res += "\treturn -1;\n"
        res += "}\n"
        return res

    def make_pyobject_type_table(self, struct_node):
        """Fill in PyTypeObject table."""
        res = "PyTypeObject " +self.type_prefix + "_" + struct_node.name + "_" + "_Type = {\n"
        code_fragments = {
        "module_name":self.namespace+"."+struct_node.name,
        "object_type":self.type_prefix + "_" + struct_node.name + "_object",
        "fn_dealloc":self.type_prefix + "_" + struct_node.name + "_object_dealloc",
        "fn_getattr":self.type_prefix + "_" + struct_node.name + "_object_getattr",
        "fn_setattr":self.type_prefix + "_" + struct_node.name + "_object_setattr",
        "docstring":struct_node.doc,
        "method_table":self.type_prefix + "_" + struct_node.name + "_object_methods",
        "member_table":self.type_prefix + "_" + struct_node.name + "_object__members",
        "fn_init":self.type_prefix + "_" + struct_node.name + "object_init",
        "fn_new":"new_" + self.type_prefix + "_" + struct_node.name

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

    def make_module_variable(self):
        header =\
"""
PyObject *module;
void init_module(PyObject *p);
"""
        body = \
"""void init_module(PyObject *p){\n
	module = p;
}
"""
        return header, body

    def mangle_type_name(self, name):
        split_name = name.split(".")
        namespace = "__".join(split_name[:-1])
        symbol = split_name[-1]
        return self.type_prefix + "_" + (namespace or self.mangled_namespace) + "_" + symbol

    def gen_type_string(self, name, node):
        """Given a name and a node, which is a type, generates a string for a variable of that type"""
        return self._gen_table[node.node_type()](self, node, name)

    def make_function(self, function):


        head = self._gen_table[function.type.return_type](self, function.type.return_type, function.name)
        args = ""
        pyargdec = ""
        boxing =""
        tuple_formatter = ""
        tuple_formatter_args=""
        for arg in function.type.args:
               args += self._gen_table[arg.type.node_type()](self, arg.type, arg.name) +", "
               pyargdec += "\tPyObject *p" +arg.name+";\n"
               boxing += "\tp" + arg.name + " = " + self.c_to_python_for_node(arg)
               tuple_formatter_args +="p"+arg.name+", "
               tuple_formatter +="O"
        args = args[0:-2]
        tuple_formatter_args = tuple_formatter_args[0:-2]
        body =""


        stubs={"head":head,
               "args":args,
               "pyargdec":pyargdec,
               "boxing":boxing,
               "tuple_formatter":tuple_formatter,
               "tuple_formatter_args":tuple_formatter_args,
               "function_name":function.name,
               "unbox": self.python_to_c_for_node(tmpnode("res", function.type.return_type))}
        res = \
"""
{head}({args}){{
    PyObject *res, *fn, args;
{pyargdec}

{boxing}
    args = Py_BuildValue("({tuple_formatter})", {tuple_formatter_args});
    if (args == NULL){{
		fprintf(stderr, "Code Gen Error: Unable to Box function \"{function_name}\" args into tuple\\n");
	}}
	fn = PyObject_GetAttrString(module, {function_name});
	if(fn == NULL){{
		fprintf(stderr, "Corresponding python function \"{function_name}\" does not exist\\n");

	}}
	res = PyObject_Call(fn, args, NULL);
	if(result ==NULL){{
		fprintf(stderr, "Error in Calling python function \"{function_name}\"\\n");
	}}
    return {unbox}

}}
""".format(**stubs)

        return res
class WrapperGenerator(object):
    def __init__(self, language):
        self.language = language
        self.plugin_stub = language.plugin_stub

    def prep(self):
        if not (os.path.exists(self.language.get_wrap_directory())):
            os.makedirs(self.language.get_wrap_directory())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        pass

    def generate(self):
        self.prep()

        c_gen = c_wrapgen.WrapperGenerator(self.language)

        c_gen.generate()
        #Write shit here.
        gen = PythonGenerator([], "", self.plugin_stub.description)
        # TODO(Clark) Implementation Order:
        # Get Pyobject, alloc and deallocing working
        # Get conversion functions generating
        c_head, c_body = gen.make_module_variable()

        for node in gen.description.declarations():
            if isinstance(node.type, pdl.TypeStruct):
                c_body += gen.make_pyobject(node) +"\n"
                c_body += gen.make_pyobject_type(node) + "\n"
                c_body += gen.make_pyobject_new(node) + "\n"
                c_body += gen.make_pyobject_dealloc(node) + "\n"
                c_body += gen.make_pyobject_hidden_dealloc(node) + "\n"
                c_body += gen.make_pyobject_to_c(node) + "\n"
                c_body += gen.make_c_to_pyobject(node) + "\n"
                c_body += gen.make_pyobject_init(node) + "\n"
                c_body += gen.make_pyobject_method_table(node) + "\n"
                c_body += gen.make_pyobject_member_table(node) + "\n"
                c_body += gen.make_pyobject_getattr(node) + "\n"
                c_body += gen.make_pyobject_setattr(node) + "\n"
                c_body += gen.make_pyobject_type_table(node) + "\n"
            elif isinstance(node.type,pdl.TypeFunction):
                c_body += gen.make_function(node)
        #print c_glue
        for node in gen.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
                c_body += gen.make_function(node)
        with open(self.language.get_c_header_filename(), "a") as f:
            f.write(c_head)

        with open(self.language.get_c_code_filename(), "w") as f:
            f.write(c_body)
