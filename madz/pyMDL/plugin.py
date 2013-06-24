"""plugin.py
@OffbyOne Studios 2013
Code for plugin description objects
"""

import re
import plugin_types as pt
class Plugin(object):
    """Object Containing description of Plugins.

    Associated with __plugin__.py files, which describe plugins.

    Attributes:
        name: String name of plugin
        version: Version of plugin
        implementation_name: String name of particular implementation of plugin interface
        language: langauge that implementation is written in
        imports: Plugins that this plugin makes use of
        depends: Plugins that this plugin require, usually providing some functionality on said plugins
        declarations: Dict of Type and Function declarations associated with this plugin
        variables: Dict Variable delcarations which require space to be allocated.
    """
    def __init__(self, **kwargs):
        self._args = kwargs

        def init_get(key, default=None):
            return self._args.get(key, default)

        self.name = init_get("name")
        self.version = init_get("version")
        self.implementation_name = init_get("implementation_name")

        self.language = init_get("language")

        self.imports = init_get("imports",[])
        self.depends = init_get("depends",[])

        self.declarations = init_get("declarations",{})
        self.variables = init_get("variables",{})


class Variable(object):
    """Data Structure for Variable Declarations.

    A Variable declaration is any declaration which requests space in memory.
        This is in contrast to Type Declarations, which define what kinds of things can request space in memory.
    """
    pass


class PluginDescription(object):
    """Data Structure for Declarations and Variables."""

    def __init__(self, declarations, variables, depends):
        """Constructor for PluginDescription helper class.

        Args:
            declarations: Dict of type definitions, whose keys are stringnames and whose values are types.
            variables: Dict of Variable declarations, whose keys are stringnames and whose values are either:
                1) keys into the declarations dict or B
                2) Anonymous types
            dependencies: Dict which maps namespaces to other plugin description objects.
        """
        self.declarations = declarations
        self.variables = variables
        self.depends = depends


    @staticmethod
    def split_namespace(stringname):
        """Splits stringname into namespace,symbol pair
        args:
            stringname: fully qualified name of symbol

        returns: (namespace, syombol) string pair.

        """
        split_name = stringname.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])
        return (namespace, end_name)


    def get_declarations_of_type(self,the_type):
        """Returns dict of all declarations matching given type.

            Args:
                the_type: plugin_type.TypeType or a subclass

            Returns:
                Dict of (identifier,type) declarations matching query
        """

        res = {}

        for key, val in self.declarations.items():
            if isinstance(val, the_type):
                res[key] = val

        return res
    def get_type(self, stringname):
        """Getter for type declarations.

        Args:
            stringname: string containing name of declaration.
        """
        namespace,symbol = self.split_namespace(stringname)
        if namespace == "":
            return self.declarations[stringname]
        else:
            # TODO Exception Checking
            return self.dependencies[namespace].description.get_type(symbol)

    def contains_type(self, stringname):
        """returns True iff stringname exist in self.declarations"""
        return self.declarations.haskey[stringname]

    def is_visible(self, stringname):
        """Returns True iff stringname exists in this namespace, or any dependant namespace."""
        if self.contains_type(self, stringname) == True:
            return True
        else:
            for name, plugin in self.depends:
                if plugin.contains_type(stringname):
                    return True
            return False
    def _validate_keys():
        c_regex ="[A-Za-z_][A-Za-z_0-9]"
        c_reserved=["auto", "else", "long", "switch", "break", "enum", "register", "typedef",
            "case", "extern", "return", "union", "char", "float", "short", " unsigned",
            "const", "for", "signed", "void",
            "continue", "goto", "sizeof", "volatile",
            "default", "if", "static", "while",
            "do", "int", "struct", "_Packed",
            "double"]

        for key in self.declarations:
            if key in c_reserved:
                raise pt.MDLSyntaxError("Keywords {} is not a valid C Identifier".format(key))

    def _validate_vals():
        for key, val in self.declarations.items():
            if val.validate() == False:
                raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
    def validate_declarations(self):
        """Checks for valid declarations."""
        def validate_typedef(t):
            if isinstance(t.type, TypeTypedef):
                return validate_typedef(t.type)
            elif isinstance(t.type, TypePointer):
                return validate_pointer(t.type)
            elif isinstance(t.type, TypeArray):
                return validate_array(t.type)
            elif isinstance(t.type, TypeStructType):
                return validate_struct(t.type)
            elif isinstance(t.type, NamedType):
                return validate_named(t.type)
            elif isinstance(t.type, TypeFunction):
                return validate_function(t.type)
            else:
                return True

        def validate_pointer(p):
            if isinstance(p.type, TypeTypedef):
                return validate_typedef(p.type)
            if isinstance(p.type, TypePointer):
                return validate_pointer(p.type)
            elif isinstance(p.type, TypeArray):
                return validate_array(p.type)
            elif isinstance(p.type, TypeStructType):
                return validate_struct(p.type)
            elif isinstance(p.type, NamedType):
                return validate_named(p.type)
            elif isinstance(p.type, TypeFunction):
                return validate_function(p.type)
            else:
                return True

        def validate_array(a):
            if isinstance(a.type, TypeTypedef):
                return validate_typedef(a.type)
            elif isinstance(a.type, TypePointer):
                return validate_pointer(a.type)
            elif isinstance(a.type, TypeArray):
                return validate_array(a.type)
            elif isinstance(a.type, TypeStructType):
                return validate_struct(a.type)
            elif isinstance(a.type, NamedType):
                return validate_named(a.type)
            elif isinstance(a.type, TypeFunction):
                return validate_function(a.type)
            else:
                return True

        def validate_struct(s):
            s.description #(str, type pairs)
            for key, val in s.description.items():
                if isinstance(val, TypeTypedef):
                    if validate_typedef(val) == False:
                        return False
                elif isinstance(val, TypePointer):
                    if validate_pointer(val) == False:
                        return False
                elif isinstance(val, TypeArray):
                    if validate_array(val) == False:
                        return False
                elif isinstance(val, TypeStructType):
                    if validate_struct(val) == False:
                        return False
                elif isinstance(val, NamedType):
                    if validate_named(val) == False:
                        return False
                elif isinstance(val, TypeFunction):
                    if validate_function(val) == False:
                        return False
                else:
                    continue
            return True
        def validate_named(n):

            return self.is_visible(n.type)
        def validate_function(f):
            n.return_type
            n.args
            if isinstance(n.return_type, TypeTypedef):
                if validate_typedef(n.return_type) == False:
                    return False
            elif isinstance(n.return_type, TypePointer):
                if validate_pointer(n.return_type) == False:
                    return False
            elif isinstance(n.return_type, TypeArray):
                if validate_array(n.return_type) == False:
                    return False
            elif isinstance(n.return_type, TypeStructType):
                if validate_struct(n.return_type) == False:
                    return False
            elif isinstance(n.return_type, NamedType):
                if validate_named(n.return_type) == False:
                    return False
            elif isinstance(n.return_type, TypeFunction):
                if validate_function(n.return_type) == False:
                    return False
            
            for key, val in n.args.items():
                if isinstance(val, TypeTypedef):
                    if validate_typedef(val) == False:
                        return False
                elif isinstance(val, TypePointer):
                    if validate_pointer(val) == False:
                        return False
                elif isinstance(val, TypeArray):
                    if validate_array(val) == False:
                        return False
                elif isinstance(val, TypeStructType):
                    if validate_struct(val) == False:
                        return False
                elif isinstance(val, NamedType):
                    if validate_named(val) == False:
                        return False
                elif isinstance(val, TypeFunction):
                    if validate_function(val) == False:
                        return False
            return True

        self._validate_keys()
        self._validate_vals()
        for key, val in self.declarations.items():
            if isinstance(val, TypeTypedef):
                if validate_typedef(val) == False:
                    raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
            elif isinstance(val, TypePointer):
                if validate_pointer(val) == False:
                    raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
            elif isinstance(val, TypeArray):
                if validate_array(val) == False:
                    raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
            elif isinstance(val, TypeStructType):
                if validate_struct(val) == False:
                    raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
            elif isinstance(val, NamedType):
                if validate_named(val) == False:
                    raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
            elif isinstance(val, TypeFunction):
                if validate_function(val) == False:
                    raise pt.MDLSyntaxError("Invalid Declaration: {} \t {}".format(key, val))
            else:
                continue
