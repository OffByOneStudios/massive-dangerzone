"""MDL/description.py
@OffbyOne Studios 2013
Provides objects for manipulating MDL descriptions.
"""

import re
import logging

from . import nodes
from . import base_types
from .extensions.objects import types as ext_objects

logger = logging.getLogger(__name__)

class NotFoundError(Exception): pass

class MDLDescription(object):
    """An object holding an MDLDescription."""

    def __init__(self, ast, dependencies):
        """Constructor for MDLDescription class.

        Args:
            ast: A list of nodes which form the description of the plugin.
            dependencies: Dictionary mapping PluginIds to MDLDescription objects.
        """
        self.ast = ast
        self.dependencies = dependencies

        # TODO: Better extension detection.
        #self.ast = ext_objects.expand(self.ast)

        self.ast = sorted(self.ast, key=self.keyfunc)

    @classmethod
    def transform_ast_named_strs(cls, ast):
        # An operation
        def str_to_named(node, name=""):
            ret_node = node
            if isinstance(node, str):
                ret_node = base_types.NamedType(node)
            if name:
                return [(name, ret_node)]
            return [ret_node]

        return cls.map_over(ast, str_to_named)

    @classmethod
    def transform_ast_user_convenience(cls, ast):
        return cls.transform_ast_named_strs(ast)

    @staticmethod
    def keyfunc(node):
        if node.node_type() == nodes.Declaration:
            return (0, node.name)
        else:
            if node.type.node_type() == base_types.TypeFunction:
                return (1, node.name)
            elif node.type.node_type() == base_types.TypePointer:
                return (2, node.name)
            else:
                return (3, node.name)

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

    def declarations(self):
        """Filters the root AST for nodes declaring new types or other information that arn't variables."""
        return list(filter(lambda n: isinstance(n, nodes.Declaration), self.ast))

    def definitions(self):
        """Filters the root AST for nodes defining new variables or other information that arn't declarations."""
        return list(filter(lambda n: isinstance(n, nodes.Definition), self.ast))

    def get_context(self, namespace):
        if namespace == "":
            return self
        return self.dependencies[namespace]

    def get_types_of(self, the_type):
        """Returns dict of all declarations matching given type.

            Args:
                the_type: plugin_type.TypeType or a subclass

            Returns:
                List of TypeDeclarations which match the type.
        """
        return filter(lambda n: isinstance(n, nodes.TypeDeclaration) and n.type == the_type, self.ast)

    def get_name_for_node(self, the_type):
        """Searches Declarations for the name of given type.

        Args:
            the_type: Node to lookup
        Returns:
            String name of the_type, otherwise the empty string
        """
        for node in self.declarations():
            if node.type == the_type:
                return node.name
        return ""

    def get_root_node(self, namespace, test_func):
        """Getter for type declarations.

        Args:
            stringname: string containing name of declaration.
        """
        if namespace == "":
            for n in self.ast:
                if test_func(n):
                    return n
        else:
            # TODO Exception Checking
            return self.dependencies[namespace].get_root_node("", test_func)
        raise NotFoundError()

    _symbol_regex = re.compile("^[A-Za-z][A-Za-z_0-9]*$")

    @classmethod
    def is_valid_symbol(cls, symbol):
        return not (cls._symbol_regex.search(symbol) is None)

    def validate(self):
        """Checks for valid declarations."""
        namespaces = {}
        for node in self.ast:
            if not (isinstance(node, nodes.Declaration) or isinstance(node, nodes.Definition)):
                logger.error("VALIDATION: Root node is not declaration or definition.")
                return False

            namespacekey = node.get_namespace_key()
            if not (namespacekey in namespaces):
                namespaces[namespacekey] = set()

            if node.name in namespaces[namespacekey]:
                logger.error("VALIDATION: Multiple names ({}) in namespace.".format(node.name))
                return False
            namespaces[namespacekey].add(node.name)

            if not (node.validate(self)):
                logger.error("VALIDATION: Node is not validated.")
                return False

        return True

    @classmethod
    def map_over(cls, ast, map_func):
        new_ast = []
        for node in ast:
            new_subs = map_func(node)
            for new_sub_node in new_subs:
                new_ast.append(new_sub_node.map_over(map_func))
        return new_ast

