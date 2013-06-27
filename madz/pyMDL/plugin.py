"""plugin.py
@OffbyOne Studios 2013
Code for plugin description objects
"""

import re
import plugin_types as base_types

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

    def __init__(self, declarations, variables, dependencies):
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
        self.dependencies = dependencies

        self._cache_validated_types = {}
        self._cache_validated_symbols = {}

        def str_to_named(node, name=""):
            ret_node = node
            if isinstance(node, basestring):
                ret_node = base_types.NamedType(node)
            if name:
                return [(name, ret_node)]
            return [ret_node]

        self.map_over(str_to_named)


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

        for key, val in self.declarations.iteritems():
            if isinstance(val, the_type):
                res[key] = val

        return res
    def get_type(self, stringname):
        """Getter for type declarations.

        Args:
            stringname: string containing name of declaration.
        """
        namespace, symbol = self.split_namespace(stringname)
        if namespace == "":
            return self.declarations[stringname]
        else:
            # TODO Exception Checking
            return self.dependencies[namespace].get_type(symbol)

    def contains_type(self, stringname):
        """returns True iff stringname exist in self.declarations"""
        return self.declarations.haskey[stringname]

    def contains_var(self, stringname):
        """returns True iff stringname exist in self.variables"""
        return self.variables.haskey[stringname]

    def is_visible_type(self, stringname):
        """Returns True iff stringname exists in this namespace, or any dependant namespace."""
        if self.contains_type(self, stringname):
            return True

        for name, description in self.dependencies.iteritems():
            if description.contains_type(stringname):
                return True

        return False

    def is_visible_var(self, stringname):
        """Returns True iff stringname exists in this namespace, or any dependant namespace."""
        if self.contains_var(self, stringname):
            return True

        for name, description in self.dependencies.iteritems():
            if description.contains_var(stringname):
                return True

        return False

    _symbol_regex = re.compile("^[A-Za-z][A-Za-z_0-9]*$")

    @classmethod
    def is_valid_symbol(cls, symbol):
        return not (cls._symbol_regex.search(symbol) is None)

    def validate_type(self, type_instance):
        if type_instance in self._cache_validated_types:
            self._cache_validated_types[type_instance]
        
        result = type_instance.validate(self)

        self._cache_validated_types[type_instance] = result

    def validate_symbol(self, symbol):
        if symbol in self._cache_validated_symbols:
            return self._cache_validated_symbols[symbol]

        result = True
        try:
            sym_type = self.get_type(symbol)
        except KeyError:
            result = False

        if not(result):
            result = sym_type.validate(self)

        self._cache_validated_symbols[symbol] = result
        return result

    def validate(self):
        """Checks for valid declarations."""
        for name, node in self.declarations.iteritems():
            if not (self.is_valid_symbol(name) and node.validate(self)):
                return False

        for name, node in self.variables.iteritems():
            if not (self.is_valid_symbol(name) and node.validate(self)):
                return False
        return True

    def map_over(self, map_func):
        new_elements = {}
        for name, node in self.declarations.iteritems():
            new_subs = map_func(node, name=name)
            for new_sub_name, new_sub_node in new_subs:
                if new_sub_name in new_elements:
                    raise InvalidTypeMDLError("Declarations can not have multiple new elements with the same name: {}".format(new_sub_name))
                new_elements[new_sub_name] = new_sub_node.map_over(map_func)
        self.declarations = new_elements

        new_elements = {}
        for name, node in self.variables.iteritems():
            new_subs = map_func(node, name=name)
            for new_sub_name, new_sub_node in new_subs:
                if new_sub_name in new_elements:
                    raise InvalidTypeMDLError("Variables can not have multiple new elements with the same name: {}".format(new_sub_name))
                new_elements[new_sub_name] = new_sub_node.map_over(map_func)
        self.variables = new_elements

