"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""
import sys,os
from collections import namedtuple
from ..c import wrapgen as c_wrapgen
# TODO(Any) Fix importing

from ... import MDL as pdl
from ...module.dependency import Dependency
from ...config import *

# Box dict elements into a named tuple so that one function can be used to construct conversions.
tmpnode = namedtuple('node', ['name', 'type'], verbose = False)

class PythonGenerator(object):
    """Class to Generate C wrapper for python plugins.

    Attributes:
        dependencies: List of python generators whose plugins this generator is dependant on
        namespace: String namespace for this plugin. Empty
        description:
        mangled_namespace:
        python_mangle:
    """

    python_mangle = "___madz_LANG_python"
    python_madz_types = "_madz_TYPE_"
    python_madz_deftypes = "_madz_DEFTYPE_"
    python_madz_types_dict = "_madz_TYPEDICT_"

    def __init__(self, dependencies, namespace, description):
        """Constructor for Python Source Generator/
        Args:
            dependencies:
                List of Python Generators whose plugins this generator is dependant on
            namespace:
                String namespace for this plugin. Empty if this generator is generating it's own plugin
            description:
                Description object given declarations and definitions
        """
        self.dependencies = dependencies
        self.namespace = namespace
        self.description = description
        self.mangled_namespace = self._namespace_mangle(namespace)

        self._is_top_level = None # Deals with self recursive structs

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

    #Python Source Generation
    def gen_type_string(self, node):
        """Given a name and a node, which is a type, generates a string for a variable of that type"""
        return self._gen_table[node.node_type()](self, node)

    def gen_type_tuple_string(self, name, node):
        """Given a name and a node, which is a type, generates a string for a variable of that type"""
        return "('{}', {})".format(name, self.gen_type_string(node))

    def _gen_table_function(self, node):
        return "CFUNCTYPE({}{})".format(
            self.gen_type_string(node.return_type),
            "" if node.args == [] else ", " + ", ".join(map(
                lambda t: "{}".format(self.gen_type_string(t.type)),
                node.args)))

    def _gen_pointer(self, node):
        return "POINTER({})".format(self.gen_type_string(node.type))

    def _gen_named(self, node):
        split = node.symbol.split(".")
        namespace = self._namespace_mangle(".".join(split[:-1])) if len(split) > 1 else self.mangled_namespace
        name = split[-1]
        return self.python_madz_types + namespace + "___" + name

    def _gen_array(self, node):
        return "({} * {})".format(self.gen_type_string(node.type), node.length)

    def _gen_table_struct(self, node):
        is_top_level = self._is_top_level
        self._is_top_level = None
        fields_list = "[{}]".format(
            ", ".join(map(
                lambda t: "{}".format(self.gen_type_tuple_string(t.name, t.type)),
                node.elements)))
        # Check if we should generate top level struct
        if not (is_top_level is None):
            return "class {name}(Structure):\n    pass\n{name}._fields_ = {fields}".format(
                name = is_top_level,
                fields = fields_list)
        else:
            return "anon_struct({})".format(fields_list)

    """Function Table for generating ctypes code from AST"""
    _gen_table = {
        pdl.TypeNone : lambda s, no: "None",
        pdl.TypeInt8 : lambda s, no: "c_byte",
        pdl.TypeInt16 : lambda s, no:"c_short",
        pdl.TypeInt32 : lambda s, no: "c_int",
        pdl.TypeInt64 : lambda s, no: "c_longlong",
        pdl.TypeChar : lambda s, no: "c_ubyte",
        pdl.TypeUInt8 : lambda s, no: "c_ubyte",
        pdl.TypeUInt16 : lambda s, no: "c_ushort",
        pdl.TypeUInt32 : lambda s, no: "c_uint",
        pdl.TypeUInt64 : lambda s, no: "c_ulonglong",
        pdl.TypeFloat32 : lambda s, no: "c_float",
        pdl.TypeFloat64 : lambda s, no: "c_double",
        pdl.TypePointer : _gen_pointer,
        pdl.TypeArray : _gen_array,
        pdl.NamedType : _gen_named,
        pdl.TypeStruct : _gen_table_struct,
        pdl.TypeFunction : _gen_table_function,
    }

    def make_typedefs(self):
        """Construct ctypes definitions for each object in AST.

        Args:
            None
        Returns:
            String containing python code to generate function.
        """
        type_dict = self.python_madz_types_dict + self.mangled_namespace
        res = "{} = {{}}\n".format(type_dict)

        for node in self.description.declarations():
            varname = self.python_madz_types + self.mangled_namespace + "___" + node.name
            # Hack to get self referential top level structs.
            if (node.type.node_type() == pdl.TypeStruct):
                self._is_top_level = varname
                res += self.gen_type_string(node.type)
                res += "\n"
            else:
                res += "{} = {}\n".format(varname, self.gen_type_string(node.type))
            res += "{}['{}'] = {}\n".format(type_dict, node.name, varname)
        return res

    def make_def_function_types(self):
        """Construct ctypes function definitions for each function in AST.

        Args:
            None
        Returns:
            String containing python code to generate function.
        """
        res = ""
        for node in self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
                res += "{} = {}\n".format(self.python_madz_deftypes + self.mangled_namespace + "___" + node.name, self.gen_type_string(node.type))

        return res

    def make_function_stubs(self):
        """Creates Python source containing a stub for functions definied in AST

        # Depreciated, no longer generating stubs for users.
        """
        res = ""
        for node in self.description.declarations() + self.description.definitions():
            if isinstance(node.type,pdl.TypeFunction):
                res += "def {}({}):\n    pass".format(node.name, ", ".join(map(
                         lambda t: "{}".format(t.name), node.type.args)) )

        return res

    def make_function_callbacks(self):
        """Constructs function callbacks to glue python functions to exported c dll functions.

        Args:
            None

        Returns:
            String to generate python source.
        """
        res = ""
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                frags={
                    "name": node.name,
                    "nameupper": self.python_madz_deftypes + "___" + node.name,
                    "sanitize": "_sanitize_python_callback" if isinstance(node.type.return_type.get_type(), pdl.TypePointer) else "_python_callback"
                }
                res += \
"""
    temp = cast({sanitize}(user_code_module.{name}, {nameupper}), {nameupper})
    keepers['{nameupper}'] = temp
    _plugin.contents.{name} = temp
""".format(**frags)
        return res

    def make_module_hook(self):
        """Hookup imported plugins so that they can be called from python

        Args:
            None
        Returns:
            String containing ctypes code to hook up plugins.
        """
        res = \
"""{fname} = shared_object.{fname}
    {fname}.restype = POINTER({structname})
    {varname} = {fname}()

"""
        fragments ={
                    "varname": self._namespace_mangle(self.namespace) + "_plugin",
                    "fname": "___madz_LANG_python_get_out_struct" if self.namespace == "" else "___madz_LANG_python_get_"+self._namespace_mangle(self.namespace) + "_struct",
                    "structname": self.python_madz_types + ("OUTSTRUCT" if self.namespace == "" else self._namespace_mangle(self.namespace))
                    }

        return res.format(**fragments)

    def make_fix_plugin(self):
        """Assigns plugin variable to point at OUTSTRUCT and not python_OUTSTRUCT"""

        res = \
"""{fname} = shared_object.{fname}
    {fname}.restype = POINTER({structname})
    {varname} = {fname}()

"""
        fragments ={
                    "varname": "_plugin",
                    "fname": "___madz_TYPE_get_out_struct",
                    "structname": self.python_madz_types + "OUTSTRUCT"
                    }

        return res.format(**fragments)

    def make_type_accessor(self, is_import):
        res = \
"""    # {dict_lookup}
    autogenerated_module.types.{dict_lookup} = _type_accessor({dictname})
    new_autogenerated_module.types.{dict_lookup} = _new_type_accessor({dictname})
"""

        fragments ={
            "dict_lookup": "self" if (is_import is None)
                else ('{reqires_type}["{name}"]'.format(
                    reqires_type = "imports" if is_import else "depends",
                    name = self.namespace)),
            "dictname": self.python_madz_types_dict + self.mangled_namespace,
            }

        return res.format(**fragments)
    def make_cleanup_code(self, is_import):
        """Creates ease of use code for end user to access imported modules.

        Args:
            None
        Returns:
            String of python cleanup code
        """
        res = \
"""    # {dict_lookup}
    autogenerated_module.{dict_lookup} = _struct_accessor({varname})
    new_autogenerated_module.{dict_lookup} = _new_struct_accessor({varname})
"""

        fragments ={
            "dict_lookup": "self" if (is_import is None)
                else ('{reqires_type}["{name}"]'.format(
                    reqires_type = "imports" if is_import else "depends",
                    name = self.namespace)),
            "varname": self.mangled_namespace + "_plugin",
            }

        return res.format(**fragments)

    # C Header Generation
    def make_c_header(self):
        """Declare interpreter threadstate and seperate struct for python function pointers.

        While a madz plugin normally has one output struct representing the plugin's variables and functions
        python plugins have two. The first contains function pointers to c functions. These functions
        aquire the python GIL, swap execution to the sub interpreter, and then call the functions in the second output
        struct. This second struct (declared below) is hooked to the python function pointers generated above.
        """
        res = \
"""PyThreadState* ___madz_LANG_python_thread_state; //Holds Thread State for this interpreter
PyObject *___madz_LANG_python_wrapper_module; //Hold Pointer to the _madz.py file representing this plugin
typedef struct{{
{function_pointers}
}}___madz_LANG_python_TYPE_;
___madz_LANG_python_TYPE_ ___madz_LANG_python_OUTPUT;
void ___madz_init_imports();
{fn_dec}

"""
        c_gen = c_wrapgen.CGenerator([],"", self.description)
        #TODO function_pointers, all same except
        fragments ={"fn_dec" : "", "function_pointers" : ""}
        fn = """{rettype}{fnname}({args});\n"""
        pointer = """    {prettype} (*{nodename})({args});\n"""
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                frg = {
                             "prettype": c_gen.gen_type_string("", node.type.return_type),
                             "rettype": c_gen.gen_type_string("", node.type.return_type),
                             "fnname": "___madz_LANG_python_FN_" + node.name,
                             "nodename": node.name,
                             "args": ",".join(map(
                                lambda a: c_gen.gen_type_string(a.name, a.type),
                                node.type.args)),

                             }
                fragments["fn_dec"] += fn.format(**frg)
                fragments["function_pointers"] += pointer.format(**frg)
        if fragments["function_pointers"] == "":
            fragments["function_pointers"] = "uint8_t _madz_empty;"
        return res.format(**fragments)

    def make_out_struct(self):
        """Ctypes Struct representing each plugin's exported struct."""
        args ={
           "name": self.python_madz_types + ("OUTSTRUCT" if self.namespace == "" else self._namespace_mangle(self.namespace)),
           "fields":""
           }

        res = \
"""class {name}(Structure):
    _fields_ = [{fields}]
"""
        for node in self.description.definitions():
            args['fields'] += self.gen_type_tuple_string(node.name, node.type) + ", "

        return res.format(**args)

    def make_get_in_struct(self):
        """Makes C function getters for in structs."""
        res = \
"""DLLEXPORT {rettype}* {prefix}_get_{name}_struct(){{
    return ___madz_IN_{name};
}}
"""
        fragments ={
                    "rettype":"___madz_TYPE_" + self._namespace_mangle(self.namespace),
                    "prefix":self.python_mangle,
                    "name":self._namespace_mangle(self.namespace)
                    }
        return res.format(**fragments)

    def make_get_python_out_struct(self):
        """Creates Getter for This plugin's python out struct."""
        res = \
"""DLLEXPORT ___madz_LANG_python_TYPE_* {}_get_out_struct(){{
    return &___madz_LANG_python_OUTPUT;
}}

"""
        return res.format(self.python_mangle)

    def make_get_out_struct(self):
        """Creates Getter for This plugin's C out struct."""
        res = \
"""DLLEXPORT ___madz_TYPE_* ___madz_TYPE_get_out_struct(){{
    return &___madz_OUTPUT;
}}

"""
        return res

    def make_c_cast_deref_string(self, c_gen, node):
        return "{}({})".format(
            "*" if node.node_type() == pdl.TypeStruct else "",
            c_gen.gen_type_string("", node))

    def make_c_init(self, madz_path):
        """Creates code to intialize this plugin's interpreter.

        This code:
            1)Confirms that the Python interpreter and Python Threads are intialized.
            2)Creates thread state for the subinterpreter
            3)Initalizes the subinterpter.
            4)Calls this plugin's python madz_init function (defined above)
        """
        res = \
"""void ___madz_init(){{
    PyObject *fn, *implib, *importer;
    PyInterpreterState *interp_state;
    PyThreadState *thread_state, *tmp;
    if(!Py_IsInitialized())
        Py_InitializeEx(0);

    if(!PyEval_ThreadsInitialized()){{
        printf("No Theadz\\n");
        PyEval_InitThreads();
    }}

    interp_state = PyInterpreterState_New();
    thread_state = PyThreadState_New(interp_state);
    PyEval_RestoreThread(thread_state);

    ___madz_LANG_python_thread_state = Py_NewInterpreter();
    tmp = PyThreadState_Swap(___madz_LANG_python_thread_state);
    implib = PyImport_ImportModule("importlib.machinery");

    fn = PyObject_GetAttrString(implib,"SourceFileLoader");
    importer = PyObject_CallObject(fn, Py_BuildValue("(ss)", "_madz", "{madzpath}"));
    Py_XDECREF(fn);
    fn = PyObject_GetAttrString(importer,"load_module");

    ___madz_LANG_python_wrapper_module = PyObject_CallObject(fn, Py_BuildValue("(s)", "_madz"));
    Py_XDECREF(fn);
    Py_XDECREF(implib);
    Py_XDECREF(importer);

    if (___madz_LANG_python_wrapper_module == NULL){{
        PyErr_Print();

        PyThreadState_Swap(tmp);
        //PyEval_SaveThread();
        return;
    }}
    fn = PyObject_GetAttrString(___madz_LANG_python_wrapper_module, "_madz_init");

    if(fn == NULL){{
        PyErr_Print();
        PyThreadState_Swap(tmp);
        //PyEval_SaveThread();

        return;
    }}

{function_hooks}

    if(PyObject_CallObject(fn, 0) == NULL){{
        PyErr_Print();
    }}

    PyThreadState_Swap(tmp);
    PyEval_SaveThread();
}}

void ___madz_init_imports(){{
    //Asks _madz.py to attach imported plugins to the madz.py autogenerated file
    PyObject *fn;
    PyThreadState *tmp;
    PyGILState_STATE gstate;

    //Swap Thread State
    tmp = PyThreadState_Swap(___madz_LANG_python_thread_state);
    //Get the init imports function
    gstate = PyGILState_Ensure();
    fn = PyObject_GetAttrString(___madz_LANG_python_wrapper_module, "_madz_init_imports");

    if(fn == NULL){{
        PyErr_Print();
        PyThreadState_Swap(tmp);
        return;
    }}
    //Call The init imports function

    if(PyObject_CallObject(fn, 0) == NULL){{
        PyErr_Print();
    }}
    PyGILState_Release(gstate);
    //Reinstate Thread State
    PyThreadState_Swap(tmp);

}}
"""
        #Path variable cannot be accessed here. Let's forward it.
        fragments = {"function_hooks":"", "madzpath" : repr(madz_path.path)[1 : -1]}
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                fragments["function_hooks"] +="    ___madz_OUTPUT." + node.name + " = " + "___madz_LANG_python_FN_" + node.name  +";\n"

        return res.format(**fragments)

    def make_c_function_stubs(self):
        """Creates function stubs wrap calls into python code.

        These functions:
            1)Swap this subinterpeter's thread in.
            2)Call into python
            3)Revert thread swap
            4)Return result
        """
        fn =\
"""{rettype} {fnname}({args}){{
    {rettype} ret;

    ret = {cast_and_deref}___madz_LANG_python_OUTPUT.{nodename}({argnames});

    return ret;
}}

"""
        fn_no_return =\
"""{rettype} {fnname}({args}){{
    ___madz_LANG_python_OUTPUT.{nodename}({argnames});
    return;
}}

"""
        res = ""
        c_gen = c_wrapgen.CGenerator([],"", self.description)
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                fragments = {
                    "maybe_parentheses": ")" if isinstance(node.type.return_type.get_type(),pdl.TypeStruct) else "",
                    "cast_and_deref": self.make_c_cast_deref_string(c_gen, node.type.return_type),
                    "rettype": c_gen.gen_type_string("", node.type.return_type),
                    "fnname": "___madz_LANG_python_FN_" + node.name,
                    "nodename": node.name,
                    "args": ",".join(map(
                        lambda a: c_gen.gen_type_string(a.name, a.type),
                        node.type.args)),
                    "argnames":",".join(map(
                        lambda a: a.name,
                        node.type.args))
                    }
                res += (fn if not isinstance(node.type.return_type, pdl.TypeTypeNone) else fn_no_return).format(**fragments)
        return res


class WrapperGenerator(c_wrapgen.WrapperGenerator):
    """Compilation object for Python.

    Attributes:
        language: Python language object.
        plugin_stub: Plugin stub attached to the Python language object.
    """
    def __init__(self, language):
        self.language = language
        self.plugin_stub = language.plugin_stub

    def prep(self):
        """Creates necessary directories for the compilation process."""
        self.language.wrap_directory

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [self.language.get_c_code_filename(),
                   self.language.get_c_header_filename(),
                   self.language.get_python_code_filename(),
                   self.language.get_python_autogenerated_module()]
        dependencies = self.language.get_source_files()
        return Dependency(dependencies, targets)

    py_template=\
"""#_madz.py
# This is an autogenerated file.

user_code_module = None
autogenerated_module = None
new_autogenerated_module = None
shared_object = None
keepers = {{}}

# Imports
import sys
import importlib.machinery
import traceback
from ctypes import *

# Helper code
def anon_struct(fields):
    class anon(Structure):
        _fields_ = fields
    return anon

# Accessors:
class _type_accessor(object):
    def __init__(self, var_dict):
        self.__var_dict = var_dict

    def __getattr__(self, name):
        if name in self.__var_dict:
            return self.__var_dict[name]
        else:
            # Default behaviour
            raise AttributeError()

class _struct_accessor(object):
    def __init__(self, pointer):
        self.__pointer = pointer

    def __getattr__(self, name):
        struct = self.__pointer.contents
        if hasattr(struct, name):
            return getattr(struct, name)
        else:
            # Default behaviour
            raise AttributeError()

def _sanitize_python_callback(func, ctypes_functype):
    sanitized_functype = CFUNCTYPE(c_void_p, *ctypes_functype._argtypes_)
    def santized_call(*args, **kwargs):
        return cast(func(*args, **kwargs), c_void_p).value
    return sanitized_functype(santized_call)

def _python_callback(func, ctypes_functype):
    return ctypes_functype(func)

# New Accessors:
try:
    _imp = importlib.machinery.SourceFileLoader("ctypes_wrapper", {ctypes_wrapper_path!r})
    ctypes_wrapper = _imp.load_module("ctypes_wrapper")
except Exception as e:
    traceback.print_exc()
    raise e

class _new_type_accessor(object):
    def __init__(self, var_dict):
        self.__var_dict = var_dict

    def __getattr__(self, name):
        if name in self.__var_dict:
            return ctypes_wrapper.internal_madz_type(self.__var_dict[name])
        else:
            # Default behaviour
            raise AttributeError()

class _new_struct_accessor(object):
    def __init__(self, pointer):
        self.__pointer = pointer

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError()

        struct = self.__pointer.contents
        if hasattr(struct, name):
            type = None
            for _name, _type in struct._fields_:
                if name == _name:
                    type = ctypes_wrapper.internal_madz_type(_type)
                    break
            if not type is None:
                return type(getattr(struct, name))
            else:
                return getattr(struct, name)
        else:
            # Default behaviour
            raise AttributeError()

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return super().__setattr__(name, value)

        struct = self.__pointer.contents
        if hasattr(struct, name):
            if hasattr(value, "__madz_object__"):
                setattr(struct, name, value.__madz_object__)
            else:
                setattr(struct, name, value)
        else:
            # Default behaviour
            raise AttributeError()

def _new_python_callback(func, ctypes_functype):
    return func

def _new_sanitize_python_callback(func, ctypes_functype):
    return _new_python_callback(func, ctypes_functype)

## Declarations

# Typedef Declarations
{typedefs}

# Dependency Function Declarations
{imported_functions}

# In_Structs
{in_structs}

# Functions
{functions}

# Exported Struct
{out_structs}

# Initilization Code

def _madz_init_imports():
    global user_code_module, autogenerated_module

    # Fill In Dependency Modules
{imp_module_hooks}

    # Clean up
    {imp_cleanup_code}

    return

def _madz_init():
    global user_code_module, autogenerated_module, new_autogenerated_module, shared_object, keepers

    sys.path.append({autogenerated_module_path!r})
    user_code_module = None
    autogenerated_module = None
    new_autogenerated_module = None

    # Get Madz DLL for this plugin
    shared_object = cdll.LoadLibrary({plugin_cname!r})
    try:
        imp = importlib.machinery.SourceFileLoader("madz", {autogenerated_module!r})
        autogenerated_module = imp.load_module("madz")
    except Exception as e:
        traceback.print_exc()
        return
    try:
        imp = importlib.machinery.SourceFileLoader("madz_future", {new_autogenerated_module!r})
        new_autogenerated_module = imp.load_module("madz_future")
    except Exception as e:
        traceback.print_exc()
        return

    {type_accessors}

    {module_hooks}

    # Fill In Dependency Modules
{dep_module_hooks}



    # Reconfigure plugin to point at real output struct
    {fix_plugin}

    # Clean up
    {dep_cleanup_code}

    {cleanup_code}

    try:
        imp = importlib.machinery.SourceFileLoader({module_namespace!r}, {init_path!r})
        user_code_module = imp.load_module({module_namespace!r})
    except Exception as e:
        traceback.print_exc()
        return

    # Fill in plugin's function pointers with callbacks
{function_callbacks}

"""

    ctypes_wrapper_template = \
'''"""ctypes_wrappers.py
@OffByOneStudios 2014

Functionality for wrapping ctypes objects into python friendly wrapper objects

As ctypes is the worst thing ever implementing plugins in python is unfun.

the goal of this library is to have an Mdl structure like:

type Gizmo{
    internal : *void,

    get_foo : (this *Gizmo)-> int32,
    set_foo : (this *Gizmo, foo int32)->void
};

Be implemented opaquely from python's perspectively ie

class GizmoInternal(madz.types["Gizmo"]):

    def __init__(self):
        self._foo = 0

    def get_foo(self):
        return self._foo

    def set_foo(self, foo):
        self._foo = int(foo)


The Actual class forms the middle layer of a ctypes, madz_types, python_types abstraction layer. It is implemented using a metaclass, a parametric class, and descriptors. The meta class is responsible for building the descriptors into instances of the parametric class, which is generated by a function taking a ctype. The descriptors provide the semantics for assigning into the ctype, and wrapping python types.
"""

#import madz
import inspect
import types
import ctypes
import _ctypes
from ctypes.util import find_library as _ctypes_find_library

# Below are helper functions for dealing with the three types of things we might encounter.

## ctypes predicates
def _ct_is_pointer_inst(instance):
    """Test if an object is an instance of a ctype pointer."""
    return isinstance(instance, _ctypes._Pointer)
def _ct_is_pointer_type(type_instance):
    """Test if an object is a subclass of a ctype pointer."""
    return inspect.isclass(type_instance) and issubclass(type_instance, _ctypes._Pointer)
def _ct_is_func_type(type_instance):
    """Test if an object is a subclass of a ctype pointer."""
    return inspect.isclass(type_instance) and issubclass(type_instance, _ctypes.CFuncPtr)
def _ct_is_structure_type(type_instance):
    """Test if an object is a subclass of a ctype pointer."""
    return inspect.isclass(type_instance) and issubclass(type_instance, _ctypes.Structure)
def _ct_typeof_pointer(pointer_type):
    """Get the type being pointed at by a ctype pointer."""
    return pointer_type._type_

def _madz_is_internal_inst(instance):
    """Test if an object is an instance of an internal madz type."""
    # Test via metaclass
    return isinstance(type(instance), InternalMadzMeta)
def _madz_is_internal_type(type_instance):
    """Test if an object is an instance of an internal madz type."""
    # Test via metaclass
    return isinstance(type_instance, InternalMadzMeta)

class InternalMadzMeta(type):
    """MetaClass for Madz_Types layer
    """
    class MadzOverrideDescriptor(object):
        """Descriptor to forward get and set calls onto the underlying ctypes structure"""
        def __init__(self, name, type_info, override=None):
            """Default Constructor

            override : Python override of the thing.
            """
            c_type, = type_info
            self._name = name
            self._override = override
            self._c_type = c_type
            self._internal_type = internal_madz_type(c_type)


        def __get__(self, instance, owner):
            """Try to get this value out of the ctype struct.

            This will try to return an object that will behave like the python object
            for the given type.
            """
            # Test for class method usage
            if instance is None:
                # Check to see if we were overriden at the class level:
                if self._override is None:
                    # We can't read from an object that doesn't exist.
                    raise NotImplementedError()
                else:
                    # We can return the override.
                    return self._override
            else:
                # Check to see if we have an override
                if self._override is None:
                    # Get the ctype object off of the ctype struct
                    res = getattr(instance.__madz_object__, self._name)
                    # If we have an internal type to cast to, cast to it, before returning
                    if self._internal_type is None:
                        return res
                    else:
                        return self._internal_type(res)
                else:
                    # If we were overriden with a callable object, call it like a method if needed:
                    if callable(self._override):
                        return types.MethodType(self._override, instance)
                    else:
                        return self._override

        def __set__(self, instance, value):
            """Try to set this value into the ctype struct.

            This will try to store the value in the ctype object.
            """
            # Test for class method usage
            if instance is None:
                # Set an override for clase values
                self._override = value
            else:
                # Check which type of object the value we are trying to set is
                if isinstance(value, ctypes._SimpleCData) or _ct_is_pointer_type(value):
                    # A simple ctype (data or pointer) just assign it.
                    pass

                elif _ct_is_func_type(value):
                    # A callable ctype, also probably, just assign it
                    pass

                # TODO: Check for ctypes structs

                elif _madz_is_internal_inst(value):
                    # A madz wrapper type.
                    value = value.__madz_object__

                else:
                    # An actual Python object.
                    # Check if it's callable
                    if callable(value) and (not type(value) is self._c_type):
                        # Assume they are attempting to assign a function with a valid sig for this slot
                        value = self._c_type(value)

                setattr(instance.__madz_object__, self._name, value)


    def __new__(meta, name, parents, attrs):
        if (not InternalMadzMeta.get_attr("__madz_ctype_is_extra_pointer__", parents, attrs)):
            InternalMadzMeta.override_attrs(InternalMadzMeta.get_attr("__madz_real_type__", parents, attrs), attrs)

        ret = type.__new__(meta, name, parents, attrs)

        return ret

    @staticmethod
    def get_attr(name, parents, attrs):
        """Helper method to retrieve attrs from parents."""
        if name in attrs:
            return attrs[name]
        for parent in parents:
            if hasattr(parent, name):
                return getattr(parent, name)
        return None

    @staticmethod
    def override_attrs(c_type, attrs):
        """Helper method to attach descriptors to every slot that needs them."""
        # Build a dict for faster lookup of ctypes fields:
        field_dict = dict(map(lambda kvp: (kvp[0], kvp[1:]), c_type._fields_))

        # Replace fields on python object:
        for attr_name, attr_val in list(attrs.items()):
            # Skip private slots:
            if attr_name.startswith("_"):
                continue
            # If it's in the ctypes object, then we want it:
            if attr_name in field_dict:
                field = field_dict[attr_name]
                attrs[attr_name] = InternalMadzMeta.MadzOverrideDescriptor(name=attr_name, type_info=field, override=attr_val)
                del field_dict[attr_name]

        # Add fields from ctype object:
        for field_name, field_val in field_dict.items():
            attrs[field_name] = InternalMadzMeta.MadzOverrideDescriptor(name=field_name, type_info=field_val)

class _HashMe(object):
    """A helper for hashing unique objects."""
    def __init__(self, obj):
        self._id = id(obj)

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, obj):
        return type(self) == type(obj) and self._id == obj._id


class _ActualBase(object): pass

_internal_madz_type_cache = dict()
def internal_madz_type(c_type):
    """Construct a Madz wrapper type from a ctype

    Args:
        c_type : A Ctype object (primative, pointer, struct, etc)
        returns : Instance of Actual, the madz wrapper class
    """

    if inspect.isclass(c_type) and issubclass(c_type, _ctypes.CFuncPtr):
        def wrap_type_this(func):
            def type_this(*args):
                args = list(map(lambda a, t : a.__madz_cast_to__(t) if hasattr(a, "__madz_cast_to__") else a, args, func._argtypes_))
                _res = func(*args)
                _type = internal_madz_type(type(_res))
                if not(_type is None):
                    return _type(_res)
                return _res
            return type_this

        return wrap_type_this

    # Skip remaining types which arn't structures or pointers to structures
    if not (_ct_is_structure_type(c_type)
            or (_ct_is_pointer_type(c_type)
                and (_ct_is_structure_type(_ct_typeof_pointer(c_type))
                    or _ct_is_pointer_type(_ct_typeof_pointer(c_type))))):
        return None

    if not _HashMe(c_type) in _internal_madz_type_cache:
        class Actual(_ActualBase, metaclass=InternalMadzMeta):
            """Implementing class for Madz_Types, the middle layer of abstraction for python plugins"""
            __madz_ctype__ = c_type
            __madz_ctype_is_pointer__ = hasattr(c_type, "_type_")
            __madz_ctype_is_extra_pointer__ = hasattr(c_type, "_type_") and hasattr(c_type._type_, "_type_")

            __madz_real_type__ = c_type._type_ if hasattr(c_type, "_type_") else c_type
            __qualname__ = c_type.__qualname__

            @classmethod
            def __madz_copy_construct__(cls, to_copy):
                res = cls()
                if issubclass(type(type(to_copy)), InternalMadzMeta):
                    res.__madz_object__ = to_copy.__madz_object__
                else:
                    # Assume that to_copy the ctypes version of cls
                    res.__madz_object__ = to_copy

                #TODO Copy field overrides?
                return res

            @classmethod
            def __madz_allocate__(cls):
                #TODO set all ctypes fields to python values.
                instance = cls.__madz_ctype__()
                if isinstance(instance, _ctypes._Pointer):
                    instance.contents = cls.__madz_ctype__._type_()
                return instance

            @classmethod
            def __madz_pointer_type__(cls):
                return internal_madz_type(ctypes.POINTER(cls.__madz_ctype__))

            def __madz_pointer_to__(self):
                _res = ctypes.pointer(self.__madz_object__)
                _type = self.__madz_pointer_type__()
                return _type(_res)

            def __madz_castable_to__(self, ctype):
                try:
                    res = self.__madz_cast_to__(ctype)
                    return not (res is None)
                except:
                    return False

            def __madz_cast_to__(self, ctype):
                if (ctype == self.__madz_ctype__):
                    return self.__madz_object__
                elif ctype is ctypes.c_void_p:
                    obj = self.__madz_object__
                    if not (self.__madz_is_pointer__):
                        obj = ctypes.pointer(self.__madz_object__)
                    return ctypes.cast(obj, ctypes.c_void_p)
                elif (hasattr(ctype, "_type_") and ctype._type_ == self.__madz_ctype__):
                    return ctype(self.__madz_object__)
                elif (hasattr(self.__madz_ctype__, "_type_") and self.__madz_ctype__._type_ == ctype):
                    return self.__madz_object__.contents
                return None

            def __init__(self, actual = None):
                #todo if ctypes is reftype set madzobject to contents, save copy of ref
                if isinstance(actual, _ActualBase):
                    actual = actual.__madz_object__
                if isinstance(actual, int):
                    actual = ctypes.c_void_p(actual)

                if (self.__madz_ctype_is_extra_pointer__):
                    self.__madz_is_pointer__ = True
                    if actual is None:
                        self.__madz_object__ = cls.__madz_ctype__()
                    elif (isinstance(actual, _ctypes._Pointer) and isinstance(actual.contents, _ctypes._Pointer)) or isinstance(actual, ctypes.c_void_p):
                        self.__madz_object__ = ctypes.cast(actual, self.__madz_ctype__)
                    else:
                        raise Exception("Cannot turn {} into deep pointer type {}".format(actual, self))
                    return

                if actual is None:
                    self.__madz_object__ = Actual.__madz_allocate__()
                    self.__madz_is_pointer__ = self.__madz_ctype_is_pointer__
                else:
                    self.__madz_is_pointer__ = isinstance(actual, _ctypes._Pointer) or isinstance(actual, ctypes.c_void_p)
                    if self.__madz_ctype_is_pointer__ and self.__madz_is_pointer__:
                        self.__madz_object__ = ctypes.cast(actual, self.__madz_ctype__)
                    elif self.__madz_ctype_is_pointer__: # and not self.__madz_is_pointer__
                        self.__madz_is_pointer__ = True
                        self.__madz_object__ = ctypes.pointer(actual)
                    elif self.__madz_is_pointer__: # and not self.__madz_ctype_is_pointer__
                        self.__madz_is_pointer__ = False
                        self.__madz_object__ = actual.contents
                    else:
                        self.__madz_object__ = actual

                self.__madz_gc__ = set()

                for field_name, _ in self.__madz_real_type__._fields_:
                    setattr(self, field_name, getattr(self, field_name))

            def __getattr__(self, name):
                if name.startswith("_"):
                    raise AttributeError("{} Attribute Error".format(name))
                elif self.__madz_ctype_is_extra_pointer__:
                    raise AttributeError("Is Deep Pointer")

                from_object = self.__madz_object__
                if self.__madz_is_pointer__:
                    if not(bool(from_object)):
                        return None
                    from_object = from_object.contents
                if hasattr(from_object, name):
                    return getattr(from_object, name)

            def __call__(self, *args, **kwargs):
                return self.__madz_object__(*args, **kwargs)

            def __nonzero__(self):
                return bool(self.__madz_object__)

        _internal_madz_type_cache[_HashMe(c_type)] = Actual

    return _internal_madz_type_cache[_HashMe(c_type)]
'''

    autogenerated_module_template = \
"""#madz.py
import ctypes as ctypes
from ctypes.util import find_library as _ctypes_find_library

class _types(object):
    def __init__(self):
        self.self = None
        self.imports = {{}}
        self.depends = {{}}

class cstdlib(object):
    _dll = ctypes.cdll.LoadLibrary(_ctypes_find_library({cstdlib}))
    malloc = _dll.malloc
    malloc.argtypes = [ctypes.c_size_t]
    malloc.restype = ctypes.c_void_p

    free = _dll.free
    free.argtypes = [ctypes.c_void_p]

class mem(object):
    @staticmethod
    def malloc(ctype):
        return ctypes.cast(cstdlib.malloc(ctypes.sizeof(ctype)), ctypes.POINTER(ctype))

    @staticmethod
    def free(ctype_ptr):
        cstdlib.free(ctypes.cast(ctype_ptr, ctypes.c_void_p))

self = None
types = _types()

def pack(obj):
    return ctypes.c_void_p(id(obj))

def unpack(pointer):
    if (pointer):
        return ctypes.cast(pointer, ctypes.py_object).value
    else:
        return None

def pointer(actual):
    try:
        if hasattr(actual, "__madz_pointer_to__"):
            return actual.__madz_pointer_to__()
        else:
            return ctypes.pointer(actual)
    except Excpetion as e:
        raise TypeError("Can only use this pointer method on actuals or ctypes.") from e

def from_str(c_thing):
    return (ctypes.cast(c_thing, ctypes.c_char_p).value).decode('utf-8')

def to_str(python_str):
    return ctypes.cast(ctypes.create_string_buffer(str.encode(python_str)), ctypes.POINTER(ctypes.c_ubyte))

imports = {{}}
depends = {{}}
"""
    def _filter_code_fragments(self, code_fragments):
        code_fragments["out_struct_func_assigns"] = ""
        code_fragments["output_var_func_declares"] = ""
        code_fragments["in_struct_imports_assigns"] +="\n\t___madz_init_imports();\n"
        code_fragments["pre_header"] = self._pre_header
        code_fragments["post_header"] = self._post_header
        return code_fragments

    def generate(self):
        """Performs the wrapping process."""
        py_gen = PythonGenerator([], "", self.plugin_stub.description)
        code_fragments = {
            "autogenerated_module_path": self.language.wrap_directory.path,
            "autogenerated_module": self.language.get_python_autogenerated_module().path,
            "new_autogenerated_module": self.language.get_python_new_autogenerated_module().path,
            "fix_plugin": py_gen.make_fix_plugin(),
            "module_namespace": "_madz__{}".format(str(self.plugin_stub.id.namespace).replace(".", "__")),
            "init_path": self.language.get_plugin_init().path,
            "ctypes_wrapper_path": self.language.get_python_ctypes_wrapper().path,
            "module_hooks": py_gen.make_module_hook(),
            "type_accessors" : py_gen.make_type_accessor(None),
            "cleanup_code": py_gen.make_cleanup_code(None),
            "imported_functions": "",
            "in_structs": "",
            "dep_module_hooks": "",
            "dep_cleanup_code": "",
            "imp_module_hooks": "",
            "imp_cleanup_code": "",
            "typedefs": "",
            "functions": py_gen.make_def_function_types(),
            "out_structs": py_gen.make_out_struct(),
            "plugin_cname": self.language.output_directory.file("{}.madz".format(self.plugin_stub.id.namespace)).path,
            "function_callbacks": py_gen.make_function_callbacks(),
            "function_stubs": py_gen.make_function_stubs()
            }

        cstdlib = {
            "windows": "'MSVCRT'",
            "unix": "'c'",
            "osx": "'c'"
        }[config_target.get(OptionPlatformOperatingSystem)]

        self.prep()
        self._pre_header ="#include \"Python.h\"\n"
        self._post_header = py_gen.make_c_header()

        c_wrapgen.WrapperGenerator.generate(self)

        c_source = py_gen.make_c_init(self.language.get_python_code_filename())
        c_source += py_gen.make_get_out_struct()
        c_source += py_gen.make_get_python_out_struct()
        c_source += py_gen.make_c_function_stubs()

        all_deps = self.plugin_stub.gen_recursive_loaded_depends()
        # depends plugins python
        for dep in all_deps:
            gen = PythonGenerator([], dep.id.namespace, dep.description)

            code_fragments["imported_functions"] += gen.make_def_function_types()
            code_fragments["typedefs"] += gen.make_typedefs()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["dep_module_hooks"] += "    " + gen.make_module_hook()
            code_fragments["dep_cleanup_code"] += "{}\n{}".format(gen.make_type_accessor(False), gen.make_cleanup_code(False))

            c_source += gen.make_get_in_struct()

        # imports plugins python
        for imp in self.plugin_stub.gen_required_loaded_imports():
            if not (imp in all_deps):
                gen = PythonGenerator([], imp.id.namespace, imp.description)

                code_fragments["imported_functions"] += gen.make_def_function_types()
                code_fragments["typedefs"] += gen.make_typedefs()
                code_fragments["in_structs"] += gen.make_out_struct()
                code_fragments["imp_module_hooks"] += "    " + gen.make_module_hook()
                code_fragments["imp_cleanup_code"] += "{}\n{}".format(gen.make_type_accessor(True), gen.make_cleanup_code(True))

                c_source += gen.make_get_in_struct()

        # This plugins python
        code_fragments["typedefs"] += py_gen.make_typedefs()

        module_string = self.autogenerated_module_template.format(cstdlib = cstdlib)
        with self.language.get_python_autogenerated_module().pyopen("w") as f:
            f.write(module_string)

        with self.language.get_python_new_autogenerated_module().pyopen("w") as f:
            f.write(module_string)

        with self.language.get_python_ctypes_wrapper().pyopen("w") as f:
            f.write(self.ctypes_wrapper_template)

        with self.language.get_c_code_filename().pyopen("a") as f:
            f.write("\n{}\n".format(c_source))

        with self.language.get_python_code_filename().pyopen("w") as f:
            f.write(self.py_template.format(**code_fragments))

    do = generate
