"""wrapgen.py
@OffbyOneStudios 2013
Code To generated C Headers from Madz Plugin Descriptions.
"""
import os

import madz.pyMDL as pdl

from madz.dependency import Dependency

class CGenerator(object):
    """Class to Generate C Headers from PyMDL

    Attributes:
        dependencies: Dict of (namespace,CGenerator) tuples
        namespace: The namespace represented by this CGenerator.
        mangled_namespace: The mangled namepace to refrenced variables in this CGenerator.
        description: The PluginDescription object this generator generates from.
    """
    def __init__(self, dependencies, namespace, description):
        """Constructor for C Generators.
        Args:
            dependencies: Dict of (namespace,CGenerator) tuples
            description: pyMDL Object containing declarions, variables, etc
        """
        self.dependencies = dependencies
        self.namespace = namespace
        self.mangled_namespace = self._namespace_mangle(namespace)
        self.description = description

    type_prefix = "___madz_TYPE"

    def _namespace_mangle(self, namespace):
        """Removes dots from namespace names, replaces them with ___"""
        return namespace.replace(".", "__")

    def _gen_table_struct(self, node, name):
        return "struct {{\n{}\n}} {}".format(
            "\n".join(map(
                lambda t: "\t{};".format(self.gen_type_string(*t)),
                node.elements.items())),
            name)

    def _gen_table_function(self, node, name):
        return "{}(*{})({})".format(
            self.gen_type_string("", node.return_type),
            name,
            ", ".join(map(
                lambda a: self.gen_type_string(a.name, a.type),
                node.args)))

    def _gen_table_typedef(self, node, name):
        return "typedef " + self.gen_type_string("", node.type) + self.type_prefix + "_" + self.namespace + "_" + name

    def _gen_actual_function(self, node, name):
        return "{}{}({})".format(
            self.gen_type_string("", node.return_type),
            name,
            ", ".join(map(
                lambda a: self.gen_type_string(a.name, a.type),
                node.args)))

    def mangle_type_name(self, name):
        split_name = name.split(".")
        namespace = "__".join(split_name[:-1])
        symbol = split_name[-1]
        return self.type_prefix + "_" + (namespace or self.mangled_namespace) + "_" + symbol

    def gen_type_string(self, name, node):
        """Given a name and a node, which is a type, generates a string for a variable of that type"""
        return self._gen_table[node.node_type()](self, node, name)

    _gen_table = {
        pdl.TypeNone : lambda s, no, na: "void ",
        pdl.TypeInt8 : lambda s, no, na: "int8_t " + na,
        pdl.TypeInt16 : lambda s, no, na: "int16_t " + na,
        pdl.TypeInt32 : lambda s, no, na: "int32_t " + na,
        pdl.TypeInt64 : lambda s, no, na: "int64_t " + na,
        pdl.TypeChar : lambda s, no, na: "char " + na,
        pdl.TypeUInt8 : lambda s, no, na: "uint8_t " + na,
        pdl.TypeUInt16 : lambda s, no, na: "uint16_t " + na,
        pdl.TypeUInt32 : lambda s, no, na: "uint32_t " + na,
        pdl.TypeUInt64 : lambda s, no, na: "uint64_t " + na,
        pdl.TypeFloat32 : lambda s, no, na: "float " + na,
        pdl.TypeFloat64 : lambda s, no, na: "double " + na,
        pdl.TypePointer : lambda s, no, na: "{} * {}".format(s.gen_type_string("", no.type), na),
        pdl.TypeArray : lambda s, no, na: "{} {}[{}]".format(s.gen_type_string("", no.type), na, no.length),
        pdl.NamedType : lambda s, no, na:"{} {}".format(s.mangle_type_name(no.symbol), na),
        pdl.TypeStruct : _gen_table_struct,
        pdl.TypeFunction : _gen_table_function,
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
        """Constructs Declarations for this namespace"""
        res = ""
        #TODO For each typedef, struct def, function defininition generate C rep
        for node in self.description.declarations():
            res += "typedef {};\n".format(self.gen_type_string(self.mangle_type_name(node.name), node.type))
        return res

    def make_variables(self):
        """Constructs a struct holding variables for this namespace."""

        res = "typedef struct{\n"
        #TODO(Put everything not a typedef here)
        for node in self.description.definitions():
            res += "\t" + self.gen_type_string(node.name, node.type) + ";\n"
        res += "}" + self.type_prefix + "_" + self.mangled_namespace + ";\n"

        return res

    def make_declares_and_vars(self):
        """Makes the c declarations and variables for this namespace."""
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

        for var in self.description.definitions():
            actual_type = get_actual_type(var.type)
            if isinstance(actual_type, pdl.TypeFunction):
                code_fragments["output_var_bindings"] += \
                    "#define MADZOUTFUNC_{} {}\n".format(
                        var.name,
                        self._gen_actual_function(actual_type, "___madz_OUTPUTFUNC_" + var.name))

                code_fragments["output_var_bindings"] += \
                    "#define MADZOUT_{} {}\n".format(
                        var.name,
                        "___madz_OUTPUTFUNC_" + var.name)

                code_fragments["output_var_func_declares"] += \
                    "MADZOUTFUNC_{};\n".format(var.name)

                code_fragments["out_struct_func_assigns"] += \
                    "___madz_OUTPUT.{} = &MADZOUT_{};\n".format(var.name, var.name)
            else:
                code_fragments["output_var_bindings"] += \
                    "#define MADZOUT_{} {}\n".format(var.name, "___madz_OUTPUT." + var.name)

class WrapperGenerator(object):
    """Responsible for driving the generation of wrapper files for C code."""

    def __init__(self, language):
        self.language = language
        self.plugin_stub = language.plugin_stub

    def prep(self):
        if not (os.path.exists(self.language.get_wrap_directory())):
            os.makedirs(self.language.get_wrap_directory())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [self.language.get_c_code_filename(),
                   self.language.get_c_header_filename()]
        dependencies = self.language.get_c_files_from()
        return Dependency(dependencies, targets)

    prefix = "___madz"
    type_prefix = "___madz_TYPE"

    def generate(self):
        self.prep()

        code_fragments = {
            "in_struct_defines" : "/* Definied structs for the incoming plugin variables */\n",
            "in_struct_declares" : "/* Declaring structs for the incoming plugin variables */\n",
            "out_struct_func_assigns" : "/* Assign functions in this plugin into the outgoing variables struct */\n",
            "in_struct_depends_assigns" : "/* Definied structs for the incoming depends plugin variables */\n\tint in_req=0;\n",
            "in_struct_imports_assigns" : "/* Definied structs for the incoming imports plugin variables */\n\tint in_req=0;\n",
            "output_var_bindings" : "/* Bindings for ease of use in c */\n",
            "output_var_func_declares" : "/* Declare output functions */\n",
            "madz_prefix" : self.prefix,
            "type_prefix" : self.type_prefix,
            "depends_declares_vars" : "",
            "imports_declares_vars" : "",
            "current_declares_vars" : "",
        }

        def make_in_struct(gen, is_dep):
            namespace = gen.mangled_namespace
            name = "___madz_IN_{namespace}".format(namespace=namespace)
            type_and_name = \
                "{type_prefix}_{namespace} * {name};\n".format(
                    type_prefix = self.type_prefix,
                    namespace = namespace,
                    name = name)
            code_fragments["in_struct_declares"] += "extern " + type_and_name
            code_fragments["in_struct_defines"] += type_and_name
            code_fragments["in_struct_depends_assigns" if is_dep else "in_struct_imports_assigns"] += \
                "\t{name} = {require_type}[in_req]; in_req += 1;\n".format(name=name, 
                    require_type="depends" if is_dep else "imports")

        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = CGenerator([], dep.id.namespace, dep.description)
            code_fragments["depends_declares_vars"] += gen.make_declares_and_vars()
            make_in_struct(gen, True)

        for imp in self.plugin_stub.loaded_imports:
            gen = CGenerator([], imp.id.namespace, imp.description)
            code_fragments["imports_declares_vars"] += gen.make_declares_and_vars()
            make_in_struct(gen, False)

        gen = CGenerator([], "", self.plugin_stub.description)
        code_fragments["current_declares_vars"] += gen.make_declares_and_vars()
        gen.build_current_output(code_fragments)

        with open(self.language.get_c_header_filename(), "w") as f:
            f.write(self.header_file_template.format(**code_fragments))

        with open(self.language.get_c_code_filename(), "w") as f:
            f.write(self.code_file_template.format(**code_fragments))

    header_file_template = \
"""
#ifndef MADZ_GAURD_WRAP_MADZ_H
#define MADZ_GAURD_WRAP_MADZ_H

#include <inttypes.h>

#define MADZ(namespace) (*{madz_prefix}_IN_##namespace)
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

//Some defines for cross platform madz dlls
#ifndef WIN32
#define __stdcall
#endif
#ifdef WIN32
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT __attribute__ ((visibility ("default")))
#endif

/* Define the outgoing variable's struct */
{type_prefix}_ {madz_prefix}_OUTPUT;

{in_struct_defines}

/* The external dll function, called by the madz plugin system, to intialize this plugin */
int DLLEXPORT {madz_prefix}_EXTERN_INIT(void * * depends, void * * output) {{
\t{out_struct_func_assigns}

\t{in_struct_depends_assigns}

\t/* Call this plugin's init function */
\t{madz_prefix}_init();

\t/* Output this plugin's variable struct */
\t(*output) = &{madz_prefix}_OUTPUT;
}}

/* The external dll function, called by the madz plugin system, to provide imports */
int DLLEXPORT {madz_prefix}_EXTERN_INITIMPORTS(void * * imports) {{
\t{in_struct_imports_assigns}
}}

"""
