import os

import shared, from_inter

class CGenerator(object):
    def __init__(self, namespace, dependencies, declarations):
        self._namespace = self._namespace_mangle(namespace)
        self._dependencies = dependencies
        self.declarations = declarations

    def _namespace_mangle(namespace):
        return namespace.replace(".", "__")

    def _dependency_generate_type_string(self, name):
        split_name = name.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])

        return self.dependencies[namespace].entry_type_string(end_name)

    def _gen_table_struct(node, name):
        s = "struct{\n"
        for k,v in val.value.items():
            s += "\t" + self.as_c_statement(name,k,v) + ";\n"
        s += "} " + function_prefix+namespace+"_" +key
        return s

    def _gen_table_function(node, name):
        ret = self.as_c_statement(name, "", val.return_type)
        ret += key + "("
        for k, v in val.args.items():
            ret += self.as_c_statement(k,v) + ", "
        ret = ret[0:len(ret)-2] + ")"
        return ret
    
    def _gen_table_typedef(node, name):
        ret = self.as_c_statement(name, "", val.return_type)
        ret += key + "("
        for k, v in val.args.items():
            ret += self.as_c_statement(k,v) + ", "
        ret = ret[0:len(ret)-2] + ")"
        return ret

    _gen_table = {
        TypeNone : lambda no, na: "void ",
        TypeInt8 : lambda no, na: "char " + na,
        TypeInt16 : lambda no, na: "short " + na,
        TypeInt32 : lambda no, na: "int " + na,
        TypeInt64 : lambda no, na: "long long " + na,
        TypeChar : lambda no, na: "char " + na,
        TypeUInt8 : lambda no, na: "unsigned char " + na,
        TypeUInt16 : lambda no, na: "unsigned short " + na,
        TypeUInt32 : lambda no, na: "unsigned int " + na,
        TypeInt64 : lambda no, na: "unsigned long long" + na,
        TypeFloat32 : lambda no, na: "float "+ na,
        TypeFloat64 : lambda no, na: "double " + na,
        TypePtr : lambda no, na: "{} * {}".format(self.generate_type_string(no.type), name),
        TypeStructType : _gen_table_struct,
        TypeFunction : _gen_table_function,
        TypeTypedef : _gen_table_typedef,
    }

    def _generate_string(self, node, name):
        return self._gen_table[node](node, name)

    def entry_string(self, name):
        return self._generate_type_string(self.declarations[name], name)

    def ordering(node):
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

    hack = \
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

        gen = from_inter.From_Inter()
        b_dir = self.get_build_directory()

        with open(os.path.join(b_dir, "madz.h"), "w") as f:
            f.write(gen.make_typedefs(self.plugin_stub))
            f.write(gen.make_structs(self.plugin_stub))
            f.write(self.hack)
