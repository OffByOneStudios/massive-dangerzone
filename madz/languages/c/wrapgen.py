"""wrapgen.py
@OffbyOneStudios 2013
Code To generated C Headers from Madz Plugin Descriptions.
"""
import os

import shared
import madz.pyMDL.plugin_types as pdl

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

    type_prefix = "___madz_TYPE"

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

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
        return "typedef " + self.gen_type_string("", node.type) + self.type_prefix + "_" + self.namespace + "_" + name

    def _gen_actual_function(self, node, name):
        return "{}{}({})".format(
            self.gen_type_string("", node.return_type),
            name,
            ", ".join(map(lambda t: self.gen_type_string(*t), node.args.items())))

    def mangle_type_name(self, name):
        split_name = name.split(".")
        namespace = "__".join(split_name[:-1])
        symbol = split_name[-1]
        return self.type_prefix + "_" + (namespace or self._namespace) + "_" + symbol

    def gen_type_string(self, name, node):
        if isinstance(node, str):
            node = pdl.NamedType(node)
        return self._gen_table[node.node_type()](self, node, name)

    _gen_table = {
        pdl.TypeNone : lambda s, no, na: "void ",
        pdl.TypeInt8 : lambda s, no, na: "char " + na,
        pdl.TypeInt16 : lambda s, no, na: "short " + na,
        pdl.TypeInt32 : lambda s, no, na: "int " + na,
        pdl.TypeInt64 : lambda s, no, na: "long long " + na,
        pdl.TypeChar : lambda s, no, na: "char " + na,
        pdl.TypeUInt8 : lambda s, no, na: "unsigned char " + na,
        pdl.TypeUInt16 : lambda s, no, na: "unsigned short " + na,
        pdl.TypeUInt32 : lambda s, no, na: "unsigned int " + na,
        pdl.TypeInt64 : lambda s, no, na: "unsigned long long" + na,
        pdl.TypeFloat32 : lambda s, no, na: "float " + na,
        pdl.TypeFloat64 : lambda s, no, na: "double " + na,
        pdl.TypePointer : lambda s, no, na: "{} * {}".format(s.gen_type_string(no.type), name),
        pdl.NamedType : lambda s, no, na:"{} {}".format(s.mangle_type_name(no.type), na),
        pdl.TypeStructType : _gen_table_struct,
        pdl.TypeFunction : _gen_table_function,
        pdl.TypeTypedef : _gen_table_typedef,
    }

    def ordering(self, node):
        node_type = node[0].__class__
        # Typedefs
        # Structs
        # Variables
        # Fucntions
        if node_type == pdl.TypeTypedef:
            return 1
        elif node_type == pdl.TypeStructType:
            return 2
        elif node_type == pdl.TypeFunction:
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

    def make_variables(self):
        """Constructs a struct holding variables for module."""

        res = "typedef struct{\n"
        #TODO(Put everything not a typedef here)
        for vname, vtype in self.variables.items():
            res += "\t" + self.gen_type_string(vname, vtype) + ";\n"
        res += "}" + self.type_prefix + "_" + self._namespace + ";\n"

        return res

    def make_declares_and_vars(self):
        declares_vars  = "/*   * NAMESPACE: {} */\n".format(self.namespace)
        declares_vars += "/*   * \> declarations */\n"
        declares_vars += self.make_declarations()
        declares_vars += "/*   * \> variables struct */\n"
        declares_vars += self.make_variables()
        declares_vars += "\n\n"

        return declares_vars

    def build_current_output(self, code_fragments):
        def get_actual_type(var_type):
            return var_type

        for var_name, var_type in self.variables.items():
            actual_type = get_actual_type(var_type)
            if isinstance(actual_type, pdl.TypeFunction):
                code_fragments["output_var_bindings"] += \
                    "#define MADZOUTFUNC_{} {}\n".format(
                        var_name,
                        self._gen_actual_function(actual_type, "___madz_OUTPUTFUNC_" + var_name))

                code_fragments["output_var_bindings"] += \
                    "#define MADZOUT_{} {}\n".format(
                        var_name,
                        "___madz_OUTPUTFUNC_" + var_name)

                code_fragments["output_var_func_declares"] += \
                    "MADZOUTFUNC_{};\n".format(var_name)

                code_fragments["out_struct_func_assigns"] += \
                    "___madz_OUTPUT.{} = &MADZOUT_{};\n".format(var_name, var_name)
            else:
                code_fragments["output_var_bindings"] += \
                    "#define MADZOUT_{} {}\n".format(var_name, "___madz_OUTPUT." + var_name)

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

    prefix = "___madz"
    type_prefix = "___madz_TYPE"

    header_file_template = \
"""
#ifndef MADZ_GAURD_WRAP_MADZ_H
#define MADZ_GAURD_WRAP_MADZ_H

#define MADZ(namespace) {madz_prefix}_IN_##namespace
#define MADZTYPE(namespace,symbol) {type_prefix}_##namespace##_##symbol

#define MADZINIT void {madz_prefix}_init()
MADZINIT;

/******************************
|********* Depends ***********|
******************************/
{depends_declares_vars}

/******************************
|********* Imports ***********|
******************************/
{imports_declares_vars}

/******************************
|********* Current ***********|
******************************/
{current_declares_vars}

{in_struct_declares}
extern {type_prefix}_ {madz_prefix}_OUTPUT;

{output_var_bindings}
{output_var_func_declares}

#endif /* MADZ_GAURD_WRAP_MADZ_H */
"""

    code_file_template = \
"""
#include<stdlib.h>

#include "madz.h"

/* Define the outgoing variable's struct */
{type_prefix}_ {madz_prefix}_OUTPUT;

{in_struct_defines}

/* The external dll function, called by the madz plugin system */
int {madz_prefix}_EXTERN_INIT(void * * dependencies, void * * requirements, void * * output) {{
    {out_struct_func_assigns}

    {in_struct_assigns}

    /* Call this plugin's init function */
    {madz_prefix}_init();

    /* Output this plugin's variable struct */
    (*output) = &{madz_prefix}_OUTPUT;
}}

"""

    def generate(self):
        self.prep()

        code_fragments = {
            "in_struct_defines" : "/* Definied structs for the incoming plugin variables */\n",
            "in_struct_declares" : "/* Declaring structs for the incoming plugin variables */\n",
            "out_struct_func_assigns" : "/* Assign functions in this plugin into the outgoing variables struct */\n",
            "in_struct_assigns" : "/* Definied structs for the incoming plugin variables */\n",
            "output_var_bindings" : "/* Bindings for ease of use in c */\n",
            "output_var_func_declares" : "/* Declare output functions */\n",
            "madz_prefix" : self.prefix,
            "type_prefix" : self.type_prefix,
            "depends_declares_vars" : "",
            "imports_declares_vars" : "",
            "current_declares_vars" : "",
        }

        def make_in_struct(gen):
            type_and_name = \
                "{type_prefix}_{namespace} ___madz_IN_{namespace};\n".format(
                    type_prefix = self.type_prefix,
                    namespace = gen._namespace)
            code_fragments["in_struct_declares"] += "extern " + type_and_name
            code_fragments["in_struct_defines"] += type_and_name

        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = CGenerator([], dep.id.namespace, dep.description)
            code_fragments["depends_declares_vars"] += gen.make_declares_and_vars()
            make_in_struct(gen)

        for imp in self.plugin_stub.loaded_imports:
            gen = CGenerator([], imp.id.namespace, imp.description)
            code_fragments["imports_declares_vars"] += gen.make_declares_and_vars()
            make_in_struct(gen)

        gen = CGenerator([], "", self.plugin_stub.description)
        code_fragments["current_declares_vars"] += gen.make_declares_and_vars()
        gen.build_current_output(code_fragments)

        with open(self.lang.get_c_header_filename(self.plugin_stub), "w") as f:
            f.write(self.header_file_template.format(**code_fragments))

        with open(self.lang.get_c_code_filename(self.plugin_stub), "w") as f:
            f.write(self.code_file_template.format(**code_fragments))
