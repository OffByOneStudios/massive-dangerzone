"""wrapgen.py
@OffbyOneStudios 2013
Code To generated C Headers from Madz Plugin Descriptions.
"""
import os
import logging
import contextlib

from ... import MDL as pdl
from ...core.dependency import Dependency

logger = logging.getLogger(__name__)

class CppCodeGenerator(object):
    def __init__(self, **kwargs):
        self.root_namespace = kwargs.get("root_namespace", "madz")
        self.type_namespace = kwargs.get("type_namespace", "_t")
        self.func_namespace = kwargs.get("func_namespace", "_f")
        self.struct_type_name = kwargs.get("struct_type_name", "_")
        self.struct_var_name = kwargs.get("struct_var_name", "_")

        self.in_type = False
        self.in_func = False
        self.in_namespace = ""

        self.with_typedef = True;

    @contextlib.contextmanager
    def in_namespace(namespace, is_type=False, is_func=False):
        old = (self.in_namespace, self.in_type, self.in_func)
        self.in_namespace = namespace
        self.in_type = is_type
        self.in_func = is_func

        yield

        self.in_namespace, self.in_type, self.in_func = old

    def _sanitize_symbol(self, symbol):
        if symbol in [
            "class", "this", "struct",
            "new", "delete",
            "if", "switch", "while", "for", "case", "break", "continue", "do"
            "align"
        ]:
            return "_" + symbol;
        else:
            return symbol;

    def _gen_table_struct(self, node, name):
        return "struct {} {{\n{}\n}} {}".format(
            ("" if self.with_typedef else name),
            "\n".join(map(
                lambda t: "\t{};".format(self.gen_node(self._sanitize_symbol(t.name), t.type)),
                node.elements)),
            (name if self.with_typedef else ""),
            )

    def _gen_table_function(self, node, name):
        return "{}(*{})({})".format(
            self.gen_node("", node.return_type),
            name,
            ", ".join(map(
                lambda a: self.gen_node(self._sanitize_symbol(a.name), a.type),
                node.args)))

    class TypeRef(pdl.TypePointer):
        pass

    _gen_table = {
        pdl.TypeNone : lambda s, no, na: "void " + na,
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
        pdl.TypePointer : lambda s, no, na: s.gen_node("* {}".format(na), no.type),
        TypeRef : lambda s, no, na: s.gen_node("& {}".format(na), no.type),
        pdl.TypeArray : lambda s, no, na: "{} {}[{}]".format(s.gen_node("", no.type), na, no.length),
        pdl.NamedType : lambda s, no, na:"{} {}".format(s.gen_ns_name(no.symbol, is_type=True), na),
        pdl.TypeStruct : _gen_table_struct,
        pdl.TypeFunction : _gen_table_function,
    }

    def gen_node(self, gend_name, node):
        return self._gen_table[node.node_type()](self, node, gend_name)

    def gen_name(self, name):
        return self._sanitize_symbol(name)

    def gen_ns_name(self, name, is_type=False, is_func=False):
        ns_list = name.split(".")
        name = self.gen_name(ns_list[-1])
        target_namespace_list = ns_list[:-1]

        if len(ns_list) == 1 :
            return "::".join(
                ([self.type_namespace] if (is_type and (not self.in_type)) else []) +
                [name])

        gend_name = "::".join(
            [self.root_namespace] +
            target_namespace_list +
            ([self.type_namespace] if is_type else []) +
            ([self.func_namespace] if is_func else []) +
            [name])
        return gend_name

    def gen_var_actual(self, struct_name, name, is_current=False):
        return ("{}.{}" if is_current else "(*{}).{}").format(
            self.gen_ns_name("{}.{}".format(
                struct_name,
                self.struct_var_name)),
            name)

    def gen_func_actual(self, struct_name, name, is_current=False):
        return ("{}.{}" if is_current else "(*{}).{}").format(
            self.gen_ns_name("{}.{}".format(
                struct_name,
                self.struct_var_name)),
            name)

    def gen_actual_function(self, name, node):
        return "{}{}({})".format(
            self.gen_node("", node.return_type),
            name,
            ", ".join(map(
                lambda a: self.gen_node(a.name, a.type),
                node.args)))


class CppNamespaceGenerator(object):
    def __init__(self, cpp_gen, namespace, description, is_current=False):
        self.gen = cpp_gen
        self.namespace = namespace
        self.description = description
        self.is_current = is_current
        if is_current:
            self._fixup_named_types()

    def _fixup_named_types(self):
        def map_func(node, name=""):
            ret_node = node
            if isinstance(node, pdl.NamedType) and \
                    len(node.symbol.split(".")) == 1:
                ret_node = pdl.NamedType("{}.{}".format(self.namespace, node.symbol))
            if name:
                return [(name, ret_node)]
            return [ret_node]

        self.description = self.description.copy()
        self.description.ast = self.description.map_over(self.description.ast, map_func)

    def _make_namespaces(self):
        return "".join(map(
            lambda ns: "namespace {} {{\n".format(ns),
            self.namespace.split('.')))

    def _make_closing_namespaces(self):
        return "".join(map(
            lambda ns: "}} /* namespace {} */\n".format(ns),
            self.namespace.split('.')))

    def _make_declarations(self):
        res = ""
        for node in self.description.declarations():
            if node.type.node_type() == pdl.TypeStruct:
                self.gen.with_typedef = False
                res += "struct {type_name};\n{declare};\n".format(
                    type_name = self.gen.gen_name(node.name),
                    declare = self.gen.gen_node(self.gen.gen_name(node.name), node.type))
                self.gen.with_typedef = True
            else:
                res += "typedef {};\n".format(self.gen.gen_node(self.gen.gen_name(node.name), node.type))
        return res

    def _make_variables_struct(self):
        #with self.gen.in_namespace("", is_type=True):
            return "typedef struct{{\n\t{};\n}} {};\n".format(
                ";\n\t".join(map(
                    lambda node: self.gen.gen_node(node.name, node.type),
                    self.description.definitions()
                )),
                self.gen.struct_type_name)

    def _make_variables_helpers(self):
        return "\t{};".format(
            ";\n\t".join(map(
                lambda node: "_MADZEXTERND({},{})".format(
                    self.gen.gen_node(node.name, self.gen.TypeRef(node.type)),
                    self.gen.gen_var_actual(self.namespace, node.name, self.is_current)),
                self.description.definitions()
            )))

    def _make_current_helpers(self):
        return "\t{};".format(
            ";\n\t".join(map(
                lambda node:
                    "_MADZEXTERND({},{})".format(
                        self.gen.gen_node(node.name, self.gen.TypeRef(node.type)),
                        self.gen.gen_var_actual(self.namespace, node.name, True)),
                self.description.definitions()
            )))

    def _make_current_actual_funcs(self):
        return "\t{};".format(
            ";\n\t".join(map(
                lambda node:
                    "{}".format(self.gen.gen_actual_function(node.name, node.type)),
                filter(lambda node: isinstance(node.type, pdl.TypeFunction), self.description.definitions())
            )))

    def make(self):
        return \
"""
{namespaces}

/* Types */
\tnamespace {type_namespace} {{
\t{decls}

\t/* Var struct */
\t{var_struct}
\t}} /* END Types */

\t_MADZEXTERN {type_namespace}::{vs_typename}{extern} {vs_name};

/* Helpers */
{helpers}
{init_if_current}
/* Actual Functions */
namespace {func_namespace} {{
{funcactual}
}} /* END Actual Functions */

{closing_namespaces}
""".format(
    type_namespace=self.gen.type_namespace,
    func_namespace=self.gen.func_namespace,
    vs_typename=self.gen.struct_type_name,
    vs_name=self.gen.struct_var_name,
    extern="" if self.is_current else "*",
    namespaces=self._make_namespaces(),
    decls=self._make_declarations(),
    var_struct=self._make_variables_struct(),
    helpers=self._make_variables_helpers(),
    init_if_current="\n/* INIT */\nvoid _init();\n" if self.is_current else "",
    funcactual=(self._make_current_actual_funcs() if self.is_current else ""),
    closing_namespaces=self._make_closing_namespaces())

    def build_current_output(self, code_fragments):
        code_fragments["output_var_bindings"] = self._make_current_helpers()

        for var in self.description.definitions():
            actual_type = var.type
            if isinstance(actual_type, pdl.TypeFunction):
                code_fragments["out_struct_func_assigns"] += \
                    "\t{} = &(MADZOUT::{func_namespace}::{});\n".format(self.gen.gen_func_actual(self.namespace, var.name, self.is_current), var.name, func_namespace=self.gen.func_namespace)

    def in_struct_assign_var(self):
        return self.gen.gen_ns_name("{}.{}".format(self.namespace, self.gen.struct_var_name));


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
        targets = [self.language.get_cpp_code_filename(),
                   self.language.get_cpp_header_filename()]
        dependencies = self.language.get_source_files()
        return Dependency(dependencies, targets)

    prefix = "___madz"

    def _filter_code_fragments(self, code_fragments):
        return code_fragments

    def generate(self):
        self.prep()

        cpp_gen = CppCodeGenerator()

        code_fragments = {
            "in_struct_defines" : "/* Definied structs for the incoming plugin variables */\n",
            "in_struct_declares" : "/* Declaring structs for the incoming plugin variables */\n",
            "out_struct_func_assigns" : "/* Assign functions in this plugin into the outgoing variables struct */\n",
            "in_struct_depends_assigns" : "/* Definied structs for the incoming depends plugin variables */\n\tint in_req=0;\n",
            "in_struct_imports_assigns" : "/* Definied structs for the incoming imports plugin variables */\n\tint in_req=0;\n",
            "output_var_bindings" : "/* Usabilitiy bindings for current namespace */\n",
            "root_namespace" : cpp_gen.root_namespace,
            "madz_prefix" : self.prefix,
            "depends_declares_vars" : "",
            "imports_declares_vars" : "",
            "current_declares_vars" : "",
            "cpp_current_namespace" : cpp_gen.gen_ns_name(self.plugin_stub.id.namespace),
        }

        def make_in_struct(gen, is_dep):
            code_fragments["in_struct_depends_assigns" if is_dep else "in_struct_imports_assigns"] += \
                "\t{name} = ({type}*){require_type}[in_req]; in_req += 1;\n".format(
                    name=gen.in_struct_assign_var(),
                    type=gen.gen.gen_ns_name("{}.{}".format(gen.namespace, gen.gen.struct_type_name), is_type=True),
                    require_type="depends" if is_dep else "imports")

        for dep in self.plugin_stub.gen_recursive_loaded_depends():
            gen = CppNamespaceGenerator(cpp_gen, dep.id.namespace, dep.description)
            code_fragments["depends_declares_vars"] += gen.make()
            make_in_struct(gen, True)

        for imp in self.plugin_stub.gen_required_loaded_imports():
            gen = CppNamespaceGenerator(cpp_gen, imp.id.namespace, imp.description)
            code_fragments["imports_declares_vars"] += gen.make()
            make_in_struct(gen, False)

        gen = CppNamespaceGenerator(cpp_gen, self.plugin_stub.id.namespace, self.plugin_stub.description, is_current=True)
        code_fragments["current_declares_vars"] += gen.make()
        gen.build_current_output(code_fragments)

        code_fragments = self._filter_code_fragments(code_fragments)

        with open(self.language.get_cpp_header_filename(), "w") as f:
            f.write(self.header_file_template.format(**code_fragments))

        with open(self.language.get_cpp_code_filename(), "w") as f:
            f.write(self.code_file_template.format(**code_fragments))

    do = generate

    header_file_template = \
"""
#ifndef MADZ_GAURD_WRAP_MADZ_H
#define MADZ_GAURD_WRAP_MADZ_H

#include <stdint.h>

#define MADZOUT {cpp_current_namespace}

/* Externing */
#ifndef _MADZEXTERN
#define _MADZEXTERN extern
#define _MADZEXTERND(sym,def) extern sym
#endif

namespace {root_namespace} {{
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

}}

{output_var_bindings}

#endif /* MADZ_GAURD_WRAP_MADZ_H */
"""

    code_file_template = \
"""
#include <stdlib.h>

#define _MADZEXTERN
#define _MADZEXTERND(sym,def) sym = def
#include "madz.h"

//Some defines for cross platform madz dlls
#ifdef _WIN32
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT __attribute__ ((visibility ("default")))
#endif

extern "C" {{
/* The external dll function, called by the madz plugin system, to intialize this plugin */
int DLLEXPORT {madz_prefix}_EXTERN_INIT(void * * depends, void * * output) {{
\t{out_struct_func_assigns}

\t{in_struct_depends_assigns}

\t/* Call this plugin's init function */
\tMADZOUT::_init();

\t/* Output this plugin's variable struct */
\t(*output) = &(MADZOUT::_);

\treturn 0;
}}

/* The external dll function, called by the madz plugin system, to provide imports */
int DLLEXPORT {madz_prefix}_EXTERN_INITIMPORTS(void * * imports) {{
\t{in_struct_imports_assigns}

\treturn 0;
}}
}}
"""
