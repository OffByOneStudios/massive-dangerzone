import os

import shared, from_inter
from  madz.pyMDL.plugin_types import *

class CGenerator(object):
    def __init__(self, dependencies, name, description):
        self.dependencies = dependencies
        self._namespace = self._namespace_mangle(name)
        self.declarations = description.declarations
        self.variables = description.variables

    type_prefix = "___MADZ_TYPE_"

    def _namespace_mangle(self, namespace):
        return namespace.replace(".", "__")

    def _dependency_generate_type_string(self, name):
        split_name = name.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])

        return self.dependencies[namespace].entry_type_string(end_name)

    def _gen_table_struct(self, node, name):
        s = "typedef struct{\n"
        for k,v in node.description.items():
            s += "\t" + self.as_c_statement(k, v) + ";\n"
        s += "} " + self.type_prefix + self._namespace + "_" + name
        return s

    def _gen_table_function(self, node, name):
        ret = self.as_c_statement(name, "", node.return_type)
        ret += name + "("
        for k, v in node.args.items():
            ret += self.as_c_statement(k,v) + ", "
        ret = ret[0:len(ret)-2] + ")"
        return ret

    def _gen_table_typedef(self, node, name):
        return "typedef " + self.as_c_statement("", node.type) + self.type_prefix + self.namespace + "_" + name

    def as_c_statement(self, name, node):
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
        TypeFloat32 : lambda s, no, na: "float "+ na,
        TypeFloat64 : lambda s, no, na: "double " + na,
        TypePointer : lambda s, no, na: "{} * {}".format(self.generate_type_string(no.type), name),
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
            res +=self.as_c_statement(name, node)
        return res

    def make_variables(self):
        """Constructs a struct holding variables for module."""
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

    hack_preamble = \
"""

"""

    hack_postamble = \
"""
#include<stdlib.h>
struct ___madz_TYPE_a * ___madz_this_output;
int ___madz_init(void * * dependencies, void * * requirements, void * * output) {
    ___madz_this_output = (struct ___madz_TYPE_a *)malloc(sizeof(___madz_TYPE_a));
    ___madz_this_output->distance = &___madz_output_distance;
    (*output) = ___madz_this_output;
}

"""

    def generate(self):
        self.prep()
        #b_dir = self.get_build_directory()
        res = ""

        for dep in self.plugin_stub.gen_recursive_loaded_depends()+self.plugin_stub.loaded_imports+[self.plugin_stub]:
            print"\n\n\n\n"
            print self.plugin_stub.id, ":", dep.id
            gen = CGenerator([], "" if dep is self.plugin_stub else dep.id.namespace, dep.description)

            print gen.make_declarations()
            #res += gen.make_declarations()
            #res += gen.make_variables()


        with open(os.path.join(self._w_dir, "madz.h"), "w") as f:
            f.write(self.hack_preamble)
            #write generated code
            f.write(self.hack_postamble)
