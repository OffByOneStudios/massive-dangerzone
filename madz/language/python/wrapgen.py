"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""
import sys,os
from collections import namedtuple
from ..c import wrapgen as c_wrapgen
# TODO(Any) Fix importing

from ... import MDL as pdl
from ...core.dependency import Dependency
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
    autogenerated_module.types.{dict_lookup} = _accessor({dictname})
"""

        fragments ={
            "dict_lookup": "self" if (is_import is None) 
                else ('{reqires_type}["{name}"]'.format(
                    reqires_type = "imports" if is_import else "depends",
                    name = self.namespace)),
            "varname": self.mangled_namespace + "_plugin",
            "dictname": self.python_madz_types_dict + self.mangled_namespace,
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
        fragments = {"function_hooks":"", "madzpath" : madz_path.replace("\\", "/")}
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
        if not (os.path.exists(self.language.get_wrap_directory())):
            os.makedirs(self.language.get_wrap_directory())

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

class _accessor(object):
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
    global user_code_module, autogenerated_module, shared_object, keepers

    sys.path.append({autogenerated_module_path!r})
    user_code_module = None
    autogenerated_module = None
    
    # Get Madz DLL for this plugin
    shared_object = cdll.LoadLibrary({plugin_cname!r})
    try:
        imp = importlib.machinery.SourceFileLoader("madz", {autogenerated_module_path!r})
        autogenerated_module = imp.load_module("madz")
    except Exception as e:
        traceback.print_exc()
        return
    
    try:
        imp = importlib.machinery.SourceFileLoader({module_namespace!r}, {init_path!r})
        user_code_module = imp.load_module({module_namespace!r})
    except Exception as e:
        traceback.print_exc()
        return
        
    {module_hooks}

    # Fill In Dependency Modules
{dep_module_hooks}

    # Fill in plugin's function pointers with callbacks
{function_callbacks}

    # Reconfigure plugin to point at real output struct
    {fix_plugin}

    # Clean up
    {dep_cleanup_code}

    {cleanup_code}
    
    
"""

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
            "autogenerated_module_path": os.path.normcase(self.language.get_python_autogenerated_module()),
            "fix_plugin": py_gen.make_fix_plugin(),
            "module_namespace": "_madz__{}!s".format(str(self.plugin_stub.id.namespace).replace(".", "__")),
            "init_path": os.path.normcase(self.language.get_plugin_init()),
            "module_hooks": py_gen.make_module_hook(),
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
            "plugin_cname": os.path.normcase(os.path.join(os.path.join(self.language.get_output_directory()), self.plugin_stub.id.namespace +".madz")),
            "function_callbacks": py_gen.make_function_callbacks(),
            "autogenerated_module_path": self.language.get_python_autogenerated_module(),
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

        # depends plugins python
        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = PythonGenerator([], dep.id.namespace, dep.description)

            code_fragments["imported_functions"] += gen.make_def_function_types()
            code_fragments["typedefs"] += gen.make_typedefs()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["dep_module_hooks"] += "    " + gen.make_module_hook()
            code_fragments["dep_cleanup_code"] += gen.make_cleanup_code(False)

            c_source += gen.make_get_in_struct()
            
        # imports plugins python   
        for imp in self.plugin_stub.gen_required_loaded_imports():
            gen = PythonGenerator([], imp.id.namespace, imp.description)

            code_fragments["imported_functions"] += gen.make_def_function_types()
            code_fragments["typedefs"] += gen.make_typedefs()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["imp_module_hooks"] += "    " + gen.make_module_hook()
            code_fragments["imp_cleanup_code"] += gen.make_cleanup_code(True)

            c_source += gen.make_get_in_struct()

        # This plugins python
        code_fragments["typedefs"] += py_gen.make_typedefs()

        with open(self.language.get_python_autogenerated_module(), "w") as f:
            f.write(self.autogenerated_module_template.format(cstdlib = cstdlib))

        with open(self.language.get_c_code_filename(), "a") as f:
            f.write("\n{}\n".format(c_source))

        with open(self.language.get_python_code_filename(), "w") as f:
            f.write(self.py_template.format(**code_fragments))

    do = generate
