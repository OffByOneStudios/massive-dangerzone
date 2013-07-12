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
        self.python_mangle = "___madz_LANG_python"

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")


    def gen_type_string(self, name, node):
        """Given a name and a node, which is a type, generates a string for a variable of that type"""
        return self._gen_table[node.node_type()](self, node, name)

    def _gen_table_function(self, node, name):
        pointer = "{}FUNC = CFUNCTYPE({}, {})".format(name.upper(), self.gen_type_string("", node.return_type),
                                                  ", ".join(map(
                lambda t: "{}".format(self.gen_type_string("", t.type)),
                node.args)))


        return pointer

    def _gen_pointer(self, node, name):

        return "(\"{}\", POINTER({}))".format(name, self.gen_type_string("", node.type))


    def _gen_table_struct(self, node, name):
        return "class {}(Structure):\n\t_fields_ = [{}]\n".format(name.upper(),
            ", ".join(map(
                lambda t: "{}".format(self.gen_type_string(*t)),
                node.elements.items())),
            )
    _gen_table = {
        pdl.TypeNone : lambda s, no, na: "None ",
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
        pdl.NamedType : lambda s, no, na: no.symbol.upper() if na =="" else "(\"{}\", {})".format(na, no.symbol.upper()),
        pdl.TypeStruct : _gen_table_struct,
        pdl.TypeFunction : _gen_table_function,
    }

    def make_structs(self):
        res = ""
        for node in self.description.declarations():
            if isinstance(node.type,pdl.TypeStruct):
                res += self.gen_type_string(node.name, node.type)

        return res

    def make_functions(self):
        res =""
        for node in self.description.declarations() + self.description.definitions():
            if isinstance(node.type,pdl.TypeFunction):
                res += self.gen_type_string(node.name, node.type) +"\n"

        return res

    def make_function_stubs(self):
        res =""
        for node in self.description.declarations() + self.description.definitions():
            if isinstance(node.type,pdl.TypeFunction):
                res += "def {}({}):\n    pass".format(node.name, ", ".join(map(
                         lambda t: "{}".format(t.name), node.type.args)) )

        return res

    def make_out_struct(self):
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
                args['fields'] += "(\"{}\" , {}),".format(node.name, node.name.upper()+"FUNC")
            else:
                args['fields'] += self.gen_type_string(node.name, node.type) +","

        return res.format(**args)

    def make_function_callbacks(self):
        res=""
        for node in self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
              res += "plugin.{} = {}FUNC(incoming_module.{})\n".format(node.name,node.name.upper(), node.name)

        return res

    def make_module_hook(self):
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


    def make_get_in_struct(self):
        """Makes Getter for in structs."""
        res = \
"""{rettype}* DLLEXPORT {prefix}_get_{name}_struct(){{
    return ___madz_IN_{name};
}}
"""
        fragments ={
                    "rettype":"___madz_TYPE_" + self._namespace_mangle(self.namespace),
                    "prefix":self.python_mangle,
                    "name":self._namespace_mangle(self.namespace)
                    }
        return res.format(**fragments)

    def make_get_out_struct(self):
        """Creates Getter for This plugin's out struct."""
        res = \
"""___madz_TYPE_* DLLEXPORT {}_get_out_struct(){{
    return &___madz_LANG_python_OUTPUT;

}}

"""
        return res.format(self.python_mangle)

    def make_c_init(self):
        res = \
"""void ___madz_init(){{
    if(Py_IsInitialized())
        fprintf(stderr,"Interpreter Is Already Initialized\\n");
    Py_Initialize();

{function_hooks}
}}
"""
        fragments={"function_hooks":""}
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                fragments["function_hooks"] +="    ___madz_OUTPUT." + node.name + " = " + node.name  +";"

        return res.format(**fragments)

    def make_cleanup_code(self):
        res = \
"""outgoing_module.imports["{name}"] = {varname}
"""
        fragments ={
                "name":self.namespace,
                "varname":self._namespace_mangle(self.namespace) + "_plugin"
                }
        return res.format(**fragments)

    def make_c_header(self):
        res = \
"""PyThreadState* python_thread_state;
___madz_TYPE_ ___madz_LANG_python_OUTPUT;
{fn_dec}
"""
        c_gen = c_wrapgen.CGenerator([],"", self.description)
        fragments ={"fn_dec" : ""}
        fn = """{rettype}{fnname}({args});"""
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                frg = {
                             "rettype":c_gen.gen_type_string("", node.type.return_type),
                             "fnname":node.name,
                             "args":",".join(map(
                                lambda a: c_gen.gen_type_string(a.name, a.type),
                                node.type.args)),

                             }
                fragments["fn_dec"] += fn.format(**frg)


        return res.format(**fragments)

    def make_c_function_stubs(self):

        fn =\
"""{rettype}{fnname}({args}){{
    {rettype}ret;
    PyThreadState* tmp_thread = PyThreadState_Swap(python_thread_state);
    ret = ___madz_LANG_python_OUTPUT.{fnname}({argnames});
    PyThreadState_Swap(tmp_thread);
    return ret;
}}

"""
        res = ""
        c_gen = c_wrapgen.CGenerator([],"", self.description)
        for node in self.description.definitions():
            if isinstance(node.type.get_type(), pdl.TypeFunction):
                fragments = {
                         "rettype":c_gen.gen_type_string("", node.type.return_type),
                         "fnname":node.name,
                         "args":",".join(map(
                            lambda a: c_gen.gen_type_string(a.name, a.type),
                            node.type.args)),
                         "argnames":",".join(map(
                            lambda a: a.name,
                            node.type.args))
                         }
                res += fn.format(**fragments)
        return res


class WrapperGenerator(c_wrapgen.WrapperGenerator):
    def __init__(self, language):
        self.language = language
        self.plugin_stub = language.plugin_stub

    def prep(self):
        if not (os.path.exists(self.language.get_wrap_directory())):
            os.makedirs(self.language.get_wrap_directory())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        pass

    py_template=\
"""#madz.py
#This is an autogenerated file.
import imp
from ctypes import *
#Dependency Function Declarations
{imported_functions}
#Dependency Structure Declarations
{imported_structs}
#Declarations
{structs}
#In_Structs
{in_structs}
#Functions
{functions}
#Exported Struct
{out_structs}
#Initilization Code
def madz_init():
    incoming_module = None
    outgoing_module = None

    try:

        with open(\"{init_path}\") as fp:
            incoming_module = imp.load_module("", fp, "", (".py", "r", imp.PY_SOURCE))

    except Exception as e:
        print("Unable to Load This Plugin's Python Functions. SegFault will occur at runtime")
        return

    try:
        with open(\"{outgoing_module_path}\") as fp:
            outgoing_module = imp.load_module("", fp, "", (".py", "r", imp.PY_SOURCE))

    except Exception as e:
        print("Generation Error: Unable to Find Outgoing Module file")
        return

    shared_object = cdll.LoadLibrary("{plugin_cname}")
    #Fill In Dependency Modules
    {module_hooks}
    #Fill in plugin's function pointers with callbacks
    {function_callbacks}
    #Clean up
    {cleanup_code}


if __name__ =='__main__':
    madz_init()
"""

    outgoing_module_template = \
"""#plugin.py
#AutoGenerated Code
#This module will contain this plugin and its import's c structures

plugin = None
imports = {}
"""
    def _filter_code_fragments(self, code_fragments):
        code_fragments["out_struct_func_assigns"] = ""
        code_fragments["output_var_func_declares"] = ""
        code_fragments["pre_header"] = self._pre_header
        code_fragments["post_header"] = self._post_header
        return code_fragments

    def generate(self):

        py_gen = PythonGenerator([], "", self.plugin_stub.description)
        code_fragments={
                        "outgoing_module_path":self.language.get_python_outgoing_module().replace("\\","/"),
                        "init_path":self.language.get_plugin_init().replace("\\","/"),
                        "imported_functions":"",
                        "imported_structs":"",
                        "in_structs":"",
                        "structs":py_gen.make_structs(),
                        "functions":py_gen.make_functions(),
                        "out_structs":py_gen.make_out_struct(),
                        "plugin_cname":os.path.join(os.path.join(self.language.get_output_directory()), self.plugin_stub.id.namespace +".madz").replace("\\","/"),
                        "function_callbacks":py_gen.make_function_callbacks(),
                        "module_hooks":py_gen.make_module_hook(),
                        "cleanup_code":"outgoing_module.plugin = plugin\n",
                        "function_stubs":py_gen.make_function_stubs()
                        }

        self.prep()
        self._pre_header ="#include \"Python.h\"\n"
        self._post_header = py_gen.make_c_header()

        c_wrapgen.WrapperGenerator.generate(self)

        c_source = py_gen.make_c_init()
        c_source += py_gen.make_get_out_struct()
        c_source += py_gen.make_c_function_stubs()


        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = PythonGenerator([], dep.id.namespace, dep.description)
            code_fragments["imported_structs"] += gen.make_structs()
            code_fragments["imported_functions"] += gen.make_functions()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["module_hooks"] +="    " + gen.make_module_hook()
            code_fragments["cleanup_code"] +="    " + gen.make_cleanup_code()
            c_source += gen.make_get_in_struct()
        for imp in self.plugin_stub.loaded_imports:
            #print imp
            gen = PythonGenerator([], imp.id.namespace, imp.description)
            #print gen.description.definitions()
            code_fragments["imported_structs"] += gen.make_structs()
            code_fragments["imported_functions"] += gen.make_functions()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["module_hooks"] += "    " + gen.make_module_hook()
            code_fragments["cleanup_code"] +="    " + gen.make_cleanup_code()
            c_source += gen.make_get_in_struct()



        with open(self.language.get_python_outgoing_module(), "w") as f:
            f.write(self.outgoing_module_template)


        with open(self.language.get_c_code_filename(), "a") as f:
            f.write("\n{}\n".format(c_source))

        with open(self.language.get_python_code_filename(), "w") as f:
            f.write(self.py_template.format(**code_fragments))

