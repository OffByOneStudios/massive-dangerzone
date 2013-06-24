"""wrapgen.py
@OffbyOneStudios 2013
Code To generated C Headers from Madz Plugin Descriptions.
"""
import os

import shared, from_inter
from  madz.pyMDL.plugin_types import *

class CGenerator(object):
    """Class to Generate C Headers from PyMDL

    Attributes:
        dependencies: Dict of (namespace,CGenerator) tuples
        namespace : str Stringname of namespace
        declarations: Dictionary of PyMDL declarations
        variables: Dictionary of PyMDL declarations
    """
    def __init__(self, dependencies, namespace, description):
        """Constructor for C Generators.
        Args:
            dependencies: Dict of (namespace,CGenerator) tuples
            description: pyMDL Object containing declarions, variables, etc
        """
        self.dependencies = dependencies
        self.namespace = namespace
        self._namespace = self._namespace_mangle(namespace)
        self.declarations = description.declarations
        self.variables = description.variables

    type_prefix = "___madz_TYPE_"

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

    def _dependency_generate_type_string(self, name):
        """# TODO (mason) What does this do wut???"""
        split_name = name.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])

        return self.dependencies[namespace].entry_type_string(end_name)

    def _gen_table_struct(self, node, name):
        return "typedef struct {{\n{}\n}} {}".format(
            "\n".join(map(lambda t: "\t{};".format(self.gen_type_string(*t)), node.description.items())),
            self.mangle_type_name(name))

    def _gen_table_function(self, node, name):
        return "{}(*{})({})".format(
            self.gen_type_string("", node.return_type),
            name,
            ", ".join(map(lambda t: self.gen_type_string(*t), node.args.items())))

    def _gen_table_typedef(self, node, name):
        return "typedef " + self.gen_type_string("", node.type) + self.type_prefix + self.namespace + "_" + name

    def _gen_actual_function(self, node, name):
        return "{}{}({})".format(
            self.gen_type_string("", node.return_type),
            name,
            ", ".join(map(lambda t: self.gen_type_string(*t), node.args.items())))

    def mangle_type_name(self, name):
        split_name = name.split(".")
        namespace = "__".join(split_name[:-1])
        symbol = split_name[-1]
        return self.type_prefix + namespace + "_" + symbol

    def gen_type_string(self, name, node):
        if isinstance(node, str):
            node = NamedType(node)
        return self._gen_table[node.node_type()](self, node, name)

    _gen_table = {
        TypeNone : lambda s, no, na: "void ",
        TypeInt8 : lambda s, no, na: "char " + na,
        TypeInt16 : lambda s, no, na: "short " + na,
        TypeInt32 : lambda s, no, na: "int " + na,
        TypeInt64 : lambda s, no, na: "long long " + na,
        TypeChar : lambda s, no, na: "char " + na,
        TypeUInt8 : lambda s, no, na: "unsigned char " + na,
        TypeUInt16 : lambda s, no, na: "unsigned short " + na,
        TypeUInt32 : lambda s, no, na: "unsigned int " + na,
        TypeInt64 : lambda s, no, na: "unsigned long long" + na,
        TypeFloat32 : lambda s, no, na: "float " + na,
        TypeFloat64 : lambda s, no, na: "double " + na,
        TypePointer : lambda s, no, na: "{} * {}".format(s.gen_type_string(no.type), name),
        NamedType : lambda s, no, na:"{} {}".format(s.mangle_type_name(no.type), na),
        TypeStructType : _gen_table_struct,
        TypeFunction : _gen_table_function,
        TypeTypedef : _gen_table_typedef,
    }

    def ordering(self, node):
        node_type = node[0].__class__
        # Typedefs
        # Structs
        # Variables
        # Fucntions
        if node_type == TypeTypedef:
            return 1
        elif node_type == TypeStructType:
            return 2
        elif node_type == TypeFunction:
            return 4
        else:
            return 3

    def make_declarations(self):
        """Constructs Declarations for module"""
        res = ""
        #TODO For each typedef, struct def, function defininition generate C rep
        for name, node in self.declarations.items():
            res += self.gen_type_string(name, node) + ";\n"
        return res

    def make_variables(self, namespace):
        """Constructs a struct holding variables for module."""
        namespace =self._namespace_mangle(namespace)

        res= ""
        if not(self.variables=={}):
            res = "typedef struct{\n"
        #TODO(Put everything not a typedef here)
            for vname, vtype in self.variables.items():
                res += "\t"+self.gen_type_string(vname, vtype)+";\n"
            res += "}" + self.type_prefix+namespace+";\n"

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

    hack_header_preamble = \
"""
#ifndef MADZ_GAURD_WRAP_MADZ_H
#define MADZ_GAURD_WRAP_MADZ_H

#define MADZTYPE(namespace,symbol) {}##namespace##_##symbol

#define MADZINIT void ___madz_INIT()
MADZINIT;
""".format(CGenerator.type_prefix)

    hack_header_postamble = \
"""
#endif /* MADZ_GAURD_WRAP_MADZ_H */
"""

    hack_code_preamble = \
"""

"""

    hack_code_postamble = \
"""
#include<stdlib.h>

#include "madz.h"

___madz_TYPE_ ___madz_OUTPUT;
int ___madz_init(void * * dependencies, void * * requirements, void * * output) {
    {}
    ___madz_INIT();
    (*output) = &___madz_OUTPUT;
}

"""

    def generate(self):
        self.prep()

        def get_actual_type(description, var_type):
                return var_type

        decsvars = ""
        for dep in self.plugin_stub.gen_recursive_loaded_depends()+self.plugin_stub.loaded_imports+[self.plugin_stub]:
            #
            #print self.plugin_stub.id, ":", dep.id
            dep_namespace = "" if dep is self.plugin_stub else dep.id.namespace

            gen = CGenerator([], dep_namespace, dep.description)

            decsvars += "/*" + ("*" * 20) + "\n" + dep_namespace +  "\n" + ("*" * 20) + "*/\n"
            decsvars += "/* declarations */\n"
            decsvars += gen.make_declarations()
            decsvars += "/* variable_struct */\n"
            decsvars += gen.make_variables("")
            decsvars += "\n\n\n"

        decsvars += "extern ___madz_TYPE_ ___madz_OUTPUT;\n\n"

        self_gen = CGenerator([], "", self.plugin_stub.description)
        self_defines = ""
        self_declares = ""
        self_functions = ""
        for var_name, var_type in self.plugin_stub.description.variables.items():
            actual_type = get_actual_type(self.plugin_stub.description, var_type)
            if isinstance(actual_type, TypeFunction):
                self_defines += "#define MADZOUTFUNC_{} {}\n".format(var_name, self_gen._gen_actual_function(actual_type, "___madz_OUTPUTFUNC_" + var_name))
                self_defines += "#define MADZOUT_{} {}\n".format(var_name, "___madz_OUTPUTFUNC_" + var_name)
                self_declares += "MADZOUTFUNC_{};\n".format(var_name)
                self_functions += "___madz_OUTPUT.{} = &MADZOUT_{};\n".format(var_name, var_name)
            else:
                self_defines += "#define MADZOUT_{} {}\n".format(var_name, "___madz_OUTPUT." + var_name)

        with open(self.lang.get_c_header_filename(self.plugin_stub), "w") as f:
            f.write(self.hack_header_preamble)
            f.write(decsvars)
            f.write(self_defines)
            f.write(self_declares)
            f.write(self.hack_header_postamble)

        with open(self.lang.get_c_code_filename(self.plugin_stub), "w") as f:
            f.write(self.hack_code_preamble)
            f.write(self.hack_code_postamble)
