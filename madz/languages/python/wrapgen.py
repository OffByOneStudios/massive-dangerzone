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


    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

    def make_function_pointers(self):
        #CFUNCTYPE(return_type, arg1_type, arg2_type)
        pass

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

        return "(POINTER({}),{})".format(name, self.gen_type_string("", node.type))


    def _gen_table_struct(self, node, name):
        return "class {}(Structure):\n\t__fields__ = [{}]\n".format(name.upper(),
            ", ".join(map(
                lambda t: "{}".format(self.gen_type_string(*t)),
                node.elements.items())),
            )
    _gen_table = {
        pdl.TypeNone : lambda s, no, na: "void ",
        pdl.TypeInt8 : lambda s, no, na: "c_byte" if na=="" else "(c_byte, \"" + na  + "\")",
        pdl.TypeInt16 : lambda s, no, na:"c_short" if na=="" else "(c_short,\"" + na + "\")",
        pdl.TypeInt32 : lambda s, no, na: "c_int" if na=="" else "(c_int, \"" + na + "\")",
        pdl.TypeInt64 : lambda s, no, na: "c_longlong" if na=="" else "(c_longlong, \"" + na + "\")",
        pdl.TypeChar : lambda s, no, na: "char" if na=="" else "(c_char, \"" + na + "\")",
        pdl.TypeUInt8 : lambda s, no, na: "c_ubyte" if na=="" else "(c_ubyte,\"" + na + "\")",
        pdl.TypeUInt16 : lambda s, no, na: "c_ushort" if na=="" else "(c_ushort, \"" + na + "\")",
        pdl.TypeUInt32 : lambda s, no, na: "c_uint" if na=="" else "(c_uint, \"" + na + "\")",
        pdl.TypeUInt64 : lambda s, no, na: "c_ulonglong" if na=="" else "(c_ulonglong, \"" + na + "\")",
        pdl.TypeFloat32 : lambda s, no, na: "c_float" if na=="" else "(c_float,\"" + na + "\")",
        pdl.TypeFloat64 : lambda s, no, na: "c_double" if na=="" else "(c_double, \"" + na + "\")",
        pdl.TypePointer : _gen_pointer,
        pdl.NamedType : lambda s, no, na: no.symbol.upper() if na =="" else "({}, {})".format(no.symbol.upper(), na),
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
                res += "def {}({}):\n\tpass".format(node.name, ", ".join(map(
                         lambda t: "{}".format(t.name), node.type.args)) )

        return res

    def make_out_struct(self):
        args ={
           "name":"OUTSTRUCT" if self.namespace=="" else self._namespace_mangle(self.namespace).upper(),
           "fields":""

           }
        res= \
"""class {name}(STRUCTURE):
    __fields__ = [{fields}]
"""
        for node in self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
                args['fields'] += "({},\"{}\")".format(node.name.upper()+"FUNC",node.name)
            else:
                args['fields'] += self.gen_type_string(node.name, node.type) +","

        return res.format(**args)

    def make_function_callbacks(self):

        res=""
        for node in self.description.definitions():
            if isinstance(node.type, pdl.TypeFunction):
              res += "plugin.{} = {}FUNC({})\n".format(node.name,node.name.upper(), node.name)

        return res

    def make_module_hook(self):
        res = "{varname} = {struct_type}.in_dll(shared_object, \"{cname}\")\n"
        fragments ={
                    "varname": "plugin" if self.namespace =="" else self._namespace_mangle(self.namespace) + "_plugin",
                    "struct_type":"OUTSTRUCT" if self.namespace == "" else self._namespace_mangle(self.namespace).upper(),
                    "cname":"___madz_OUTPUT" if self.namespace == "" else "___MADZ_IN_" + self._namespace_mangle(self.namespace)
                    }

        return res.format(**fragments)

    def make_c_init(self):
        res = \
"""void ___madz_init(){
    //# TODO(MADZ) Something useful
}
"""
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
    shared_object = cdll.LoadLibrary("{plugin_cname}")
    #Fill In Dependency Modules
    {module_hooks}
    #Fill in plugin's function pointers with callbacks
    {function_callbacks}
    #Clean up
    {cleanup_code}
#Fill In These Functions
{function_stubs}
"""
    def _filter_code_fragments(self, code_fragments):
        code_fragments["out_struct_func_assigns"] = ""
        code_fragments["output_var_func_declares"] = ""
        return code_fragments

    def generate(self):

        py_gen =PythonGenerator([], "", self.plugin_stub.description)
        code_fragments={
                        "imported_functions":"",
                        "imported_structs":"",
                        "in_structs":"",
                        "structs":py_gen.make_structs(),
                        "functions":py_gen.make_functions(),
                        "out_structs":py_gen.make_out_struct(),
                        "plugin_cname":os.path.join(os.path.join(self.language.get_output_directory()), self.plugin_stub.id.namespace +".madz"),
                        "function_callbacks":py_gen.make_function_callbacks(),
                        "module_hooks":py_gen.make_module_hook(),
                        "cleanup_code":"#TODO(MADZ) Box this into somthing nice",
                        "function_stubs":py_gen.make_function_stubs()
                        }

        self.prep()
        c_wrapgen.WrapperGenerator.generate(self)
        c_source = py_gen.make_c_init()

        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = PythonGenerator([], dep.id.namespace, dep.description)
            code_fragments["imported_structs"] += gen.make_structs()
            code_fragments["imported_functions"] += gen.make_functions()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["module_hooks"] +="\t" +  gen.make_module_hook()
        for imp in self.plugin_stub.loaded_imports:
            #print imp
            gen = PythonGenerator([], imp.id.namespace, imp.description)
            #print gen.description.definitions()
            code_fragments["imported_structs"] += gen.make_structs()
            code_fragments["imported_functions"] += gen.make_functions()
            code_fragments["in_structs"] += gen.make_out_struct()
            code_fragments["module_hooks"] += "\t" + gen.make_module_hook()


        with open(self.language.get_c_code_filename(), "a") as f:
            f.write("\n{}\n".format(c_source))

        with open(self.language.get_python_code_filename(), "w") as f:
            f.write(self.py_template.format(**code_fragments))

