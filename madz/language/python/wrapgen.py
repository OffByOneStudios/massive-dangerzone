"""wrapgen.py
@OffbyOneStudios 2013
Code To generated Python "Headers" from Madz Plugin Descriptions.
"""
import sys,os
from collections import namedtuple
from ..c import wrapgen as c_wrapgen
#import language
# TODO(Any) Fix importing

from ... import MDL as pdl
from ...core.dependency import Dependency

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
        self.python_mangle = "___madz_LANG_python"

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

    #Python Source Generation
    def gen_type_string(self, name, node):
        """Given a name and a node, which is a type, generates a string for a variable of that type"""
        return self._gen_table[node.node_type()](self, node, name)

    def _gen_table_function(self, node, name):
        """Generate Python Function Declaration.
        Args:
            node:
                AST Node object
            name:
                String function name

        Returns:
            String containing python code to generate function declaration
        """
        if isinstance(node.return_type.get_type(), pdl.TypeStruct):
            ret = "c_void_p"
        else:
            ret = self.gen_type_string("", node.return_type).strip()
        pointer = "{} = CFUNCTYPE({}{})".format("_madz_LANG_python_TYPEFUNC_" + name, ret, "" if node.args == [] else ", " + ", ".join(map(
                lambda t: "{}".format(self.gen_type_string("", t.type)),
                node.args)))
        return pointer

    def _gen_pointer(self, node, name):
        """Generates a Python Ctypes Pointer declaration for a pointer AST node.
        Args:
            node:
                AST Node object
            name:
                String pointer name
        Returns:
            String containing python code to generate pointer declaration
        """
        return "(\"{}\", POINTER({}))".format(name, self.gen_type_string("", node.type))

    def _gen_named(self, node, name):
        """Generate Python Array Definition
        no.symbol.upper() if na =="" else "(\"{}\", {})".format(na, no.symbol.upper())
        Args:
            node:
                AST Node object
            name:
                String struct name
        Returns:
            String containing python code to generate struct declaration
        """

        if isinstance(node.get_type(), pdl.TypeStruct):
            res = node.symbol.upper() if name == "" else "(\"{}\", {})".format(name, node.symbol.upper())
        elif isinstance(node.get_type(), pdl.TypeArray):
            res = "{}ArrayType".format(self.description.get_name_for_node(node.get_type())) if name == "" else  "(\"{}\", {}ArrayType)".format(
                                                                                                                                        name, self.description.get_name_for_node(node.get_type()))
        else:
            res = self.gen_type_string(name, node.get_type())
        return res

    def _gen_array(self, node, name):
        typename = self.description.get_name_for_node(node)
        if typename !="":
            return  "{}ArrayType".format(typename) if name == "" else  "(\"{}\", {}ArrayType)".format(name, typename)
        else:
            return "{} * {}".format(self.gen_type_string("", node.type), node.length) if name =="" else  "(\"{}\", {} * {})".format(name, self.gen_type_string("", node.type), node.length)

    def _gen_table_struct(self, node, name):
        """Generate Python structure definition

        Args:
            node:
                AST Node object
            name:
                String struct name
        Returns:
            String containing python code to generate struct declaration
        """

        return "class {}(Structure):\n\t_fields_ = [{}]\n".format(name.upper(),
            ", ".join(map(
                lambda t: "{}".format(self.gen_type_string(t.name, t.type)),
                node.elements)),
            )
    """Function Table for generating ctypes code from AST"""
    _gen_table = {
        pdl.TypeNone : lambda s, no, na: "None",
        pdl.TypeInt8 : lambda s, no, na: "c_byte" if na=="" else "(\"" + na  + "\" , c_byte)",
        pdl.TypeInt16 : lambda s, no, na:"c_short" if na=="" else "(\"" + na + "\", c_short)",
        pdl.TypeInt32 : lambda s, no, na: "c_int" if na=="" else "(\"" + na + "\", c_int)",
        pdl.TypeInt64 : lambda s, no, na: "c_longlong" if na=="" else "(\"" + na + "\",c_longlong)",
        pdl.TypeChar : lambda s, no, na: "char" if na=="" else "(\"" + na + "\", c_char)",
        pdl.TypeUInt8 : lambda s, no, na: "c_ubyte" if na=="" else "(\"" + na + "\", c_ubyte)",
        pdl.TypeUInt16 : lambda s, no, na: "c_ushort" if na=="" else "(\"" + na + "\", c_ushort)",
        pdl.TypeUInt32 : lambda s, no, na: "c_uint" if na=="" else "(\"" + na + "\", c_uint)",
        pdl.TypeUInt64 : lambda s, no, na: "c_ulonglong" if na=="" else "(\"" + na + "\", c_ulonglong)",
        pdl.TypeFloat32 : lambda s, no, na: "c_float" if na=="" else "(\"" + na + "\", c_float)",
        pdl.TypeFloat64 : lambda s, no, na: "c_double" if na=="" else "(\"" + na + "\", c_double)",
        pdl.TypePointer : _gen_pointer,
        pdl.TypeArray : _gen_array,
        pdl.NamedType : _gen_named,
        pdl.TypeStruct : _gen_table_struct,
        pdl.TypeFunction : _gen_table_function,
    }

    def make_typedefs(self):
        """Sets up not struct/array typedefs as variable alias of primitive ctypes."""
        res =""
        for node in self.description.declarations():
            if isinstance(node.type, pdl.TypeInt):
                res += "{} = {}\n".format(node.name, self.gen_type_string("", node.type))
            elif isinstance(node.type, pdl.TypeUInt):
                res += "{} = {}\n".format(node.name, self.gen_type_string("", node.type))
            elif isinstance(node.type, pdl.TypeFloat):
                res += "{} = {}\n".format(node.name, self.gen_type_string("", node.type))

        return res


    def make_arrays(self):
        """Construct Python Array Types for each array definition in AST/
        Args:
            None
        Returns:
            String containing python code to generate array.
        """
        res =""
        for node in self.description.declarations():
            if isinstance(node.type, pdl.TypeArray):
                res += node.name + "ArrayType = " + self.gen_type_string("", node.type.type) + "* " + str(node.type.length) + "\n"
        return res

    def make_structs(self):
        """Construct Python classes for each struct definition in AST.

        Args:
            None
        Returns:
            String containing python code to generate struct.
        """
        res = ""


        for node in self.description.declarations():
            if isinstance(node.type, pdl.TypeStruct):
                res += self.gen_type_string(node.name, node.type)
        return res

    def make_functions(self):
        """Construct ctypes function definitions for each function in AST.

        Args:
            None
        Returns:
            String containing python code to generate function.
        """
        res =""
        for node in self.description.declarations() + self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
                res += self.gen_type_string(node.name, node.type) +"\n"

        return res

    def make_function_stubs(self):
        """Creates Python source containing a stub for functions definied in AST

        # Depreciated, no longer generating stubs for users.
        """
        res =""
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
        res=""
        for node in self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
                frags={
                    "name" : node.name,
                    "nameupper" : "_madz_LANG_python_TYPEFUNC_" + node.name,
                    "args":",".join([i.name for i in node.type.args])
                }
                if isinstance(node.type.return_type.get_type(),pdl.TypeStruct):
                    res += "    plugin.contents.{name} = {nameupper}(lambda {args}:cast(byref(user_code_module.{name}({args})), c_void_p))\n".format(**frags)
                else:
                    res += "    plugin.contents.{name} = {nameupper}(user_code_module.{name})\n".format(**frags)

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
                    "varname": "plugin" if self.namespace == "" else self._namespace_mangle(self.namespace) + "_plugin",
                    "fname":"___madz_LANG_python_get_out_struct" if self.namespace == "" else "___madz_LANG_python_get_"+self._namespace_mangle(self.namespace) + "_struct",
                    "structname":"OUTSTRUCT" if self.namespace == "" else self._namespace_mangle(self.namespace).upper()
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
                    "varname": "plugin",
                    "fname":"___madz_TYPE_get_out_struct",
                    "structname":"OUTSTRUCT"
                    }

        return res.format(**fragments)

        return res
    def make_cleanup_code(self):
        """Creates ease of use code for end user to access imported modules.

        Args:
            None
        Returns:
            String of python cleanup code
        """
        res = \
"""autogenerated_module.imports["{name}"] = {varname}
"""
        fragments ={
                "name":self.namespace,
                "varname":self._namespace_mangle(self.namespace) + "_plugin"
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
                             "prettype":"void*" if isinstance(node.type.return_type.get_type(),pdl.TypeStruct) else c_gen.gen_type_string("", node.type.return_type),
                             "rettype":c_gen.gen_type_string("", node.type.return_type),
                             "fnname":"___madz_LANG_python_FN_" + node.name,
                             "nodename": node.name,
                             "args":",".join(map(
                                lambda a: c_gen.gen_type_string(a.name, a.type),
                                node.type.args)),

                             }
                fragments["fn_dec"] += fn.format(**frg)
                fragments["function_pointers"] += pointer.format(**frg)
        return res.format(**fragments)

    def make_out_struct(self):
        """Ctypes Struct representing each plugin's exported struct."""
        args ={
           "name":"OUTSTRUCT" if self.namespace=="" else self._namespace_mangle(self.namespace).upper(),
           "fields":""

           }
        res= \
"""class {name}(Structure):
    _fields_ = [{fields}]
"""
        for node in self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
                args['fields'] += "(\"{}\" , {}),".format(node.name, "_madz_LANG_python_TYPEFUNC_" + node.name)
            else:
                args['fields'] += self.gen_type_string(node.name, node.type) +","

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

    def make_cleanup_code(self):
        res =\
"""autogenerated_module.plugin = plugin
"""
        return res
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
    PyObject *name, *fn, *implib, *importer;
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
"""{rettype}{fnname}({args}){{
    {rettype}ret;
    PyThreadState *tmp;

    tmp = PyThreadState_Swap(___madz_LANG_python_thread_state);
    ret = {cast_and_deref}___madz_LANG_python_OUTPUT.{fnname}({argnames});
    PyThreadState_Swap(tmp);
    return ret;
}}

"""
        fn_no_return =\
"""{rettype}{fnname}({args}){{
    PyThreadState *tmp;

    tmp = PyThreadState_Swap(___madz_LANG_python_thread_state);
    ___madz_LANG_python_OUTPUT.{nodename}({argnames});
    PyThreadState_Swap(tmp);
    return;
}}

"""
        res = ""
        c_gen = c_wrapgen.CGenerator([],"", self.description)
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                fragments = {
                         "maybe_parentheses":")"  if isinstance(node.type.return_type.get_type(),pdl.TypeStruct) else "",
                         "cast_and_deref":"*({}*)".format(c_gen.gen_type_string("", node.type.return_type)) if isinstance(node.type.return_type.get_type(),pdl.TypeStruct) else "",
                         "rettype":c_gen.gen_type_string("", node.type.return_type),
                         "fnname":"___madz_LANG_python_FN_" + node.name,
                         "nodename": node.name,
                         "args":",".join(map(
                            lambda a: c_gen.gen_type_string(a.name, a.type),
                            node.type.args)),
                         "argnames":",".join(map(
                            lambda a: a.name,
                            node.type.args))
                         }
                res += fn.format(**fragments) if not isinstance(node.type.return_type, pdl.TypeTypeNone) else fn_no_return.format(**fragments)
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
        pass

    py_template=\
"""#_madz.py
user_code_module = None
autogenerated_module = None
#This is an autogenerated file.
import sys
import importlib.machinery
from ctypes import *
#Dependency Function Declarations
{imported_functions}
#Dependency Structure Declarations
{imported_structs}

#Declarations
#Typedef Declarations
{typedefs}
#Array Declarations
{arrays}
#Struct Declarations
{structs}
#In_Structs
{in_structs}
#Functions
{functions}
#Exported Struct
{out_structs}
#Initilization Code

def _madz_init_imports():
    global user_code_module, autogenerated_module
    print("I would init imports if I knew what you were talking abotu yet")
    return
    
def _madz_init():
    global user_code_module, autogenerated_module
    sys.path.append("{autogenerated_module_path}")
    user_code_module = None
    autogenerated_module = None
    
    #Get Madz DLL for this plugin
    shared_object = cdll.LoadLibrary("{plugin_cname}")
    try:
        imp = importlib.machinery.SourceFileLoader("madz", \"{autogenerated_module_path}\")
        autogenerated_module = imp.load_module("madz")
    except Exception as e:
        print(e)
        return
    
    try:
        imp = importlib.machinery.SourceFileLoader("__init__", \"{init_path}\")
        user_code_module = imp.load_module("__init__")
    except Exception as e:
        print(e)
        return
        
    #Fill In Dependency Modules
    {module_hooks}
    #Fill in plugin's function pointers with callbacks
{function_callbacks}
    #Reconfigure plugin to point at real output struct
    {fix_plugin}
    #Clean up
    {cleanup_code}
    #Append the outgoing module file to the system path
    
    
"""

    autogenerated_module_template = \
"""#plugin.py
#AutoGenerated Code
#This module will contain this plugin and its import's c structures
import _madz as _d
declarations = _d
plugin = None
imports = {}
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
        code_fragments={
                        "autogenerated_module_path":self.language.get_python_autogenerated_module().replace("\\","/"),
                        "fix_plugin" : py_gen.make_fix_plugin(),
                        "init_path":self.language.get_plugin_init().replace("\\","/"),
                        "imported_functions":"",
                        "imported_structs":"",
                        "in_structs":"",
                        "typedefs":py_gen.make_typedefs(),
                        "arrays" : py_gen.make_arrays(),
                        "structs":py_gen.make_structs(),
                        "functions":py_gen.make_functions(),
                        "out_structs":py_gen.make_out_struct(),
                        "plugin_cname":os.path.join(os.path.join(self.language.get_output_directory()), self.plugin_stub.id.namespace +".madz").replace("\\","/"),
                        "function_callbacks":py_gen.make_function_callbacks(),
                        "module_hooks":py_gen.make_module_hook(),
                        "cleanup_code":py_gen.make_cleanup_code(),
                        "autogenerated_module_path":self.language.get_python_autogenerated_module(),
                        "function_stubs":py_gen.make_function_stubs()
                        }

        self.prep()
        self._pre_header ="#include \"Python.h\"\n"
        self._post_header = py_gen.make_c_header()

        c_wrapgen.WrapperGenerator.generate(self)

        c_source = py_gen.make_c_init(self.language.get_python_code_filename())
        c_source += py_gen.make_get_out_struct()
        c_source += py_gen.make_get_python_out_struct()
        c_source += py_gen.make_c_function_stubs()


        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = PythonGenerator([], dep.id.namespace, dep.description)
            code_fragments["imported_structs"] += gen.make_structs()
            code_fragments["imported_functions"] += gen.make_functions()
            code_fragments["typedefs"] += gen.make_typedefs()
            code_fragments["arrays"] += gen.make_arrays()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["module_hooks"] +="    " + gen.make_module_hook()
            code_fragments["cleanup_code"] +="    " + gen.make_cleanup_code()
            c_source += gen.make_get_in_struct()
            
            
        for imp in self.plugin_stub.loaded_imports:

            gen = PythonGenerator([], imp.id.namespace, imp.description)

            code_fragments["imported_structs"] += gen.make_structs()
            code_fragments["imported_functions"] += gen.make_functions()
            code_fragments["typedefs"] += gen.make_typedefs()
            code_fragments["arrays"] += gen.make_arrays()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["module_hooks"] += "    " + gen.make_module_hook()
            code_fragments["cleanup_code"] +="    " + gen.make_cleanup_code()
            c_source += gen.make_get_in_struct()



        with open(self.language.get_python_autogenerated_module(), "w") as f:
            f.write(self.autogenerated_module_template)


        with open(self.language.get_c_code_filename(), "a") as f:
            f.write("\n{}\n".format(c_source))

        with open(self.language.get_python_code_filename(), "w") as f:
            f.write(self.py_template.format(**code_fragments))

    do = generate