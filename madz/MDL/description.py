"""MDL/description.py
@OffbyOne Studios 2013
Provides objects for manipulating MDL descriptions.
"""

import re
import os
import logging
import contextlib
import pickle

from . import nodes
from . import base_types
from .extensions.objects import types as ext_objects
from .loaders import *
from .parser_impl import generate_parser, get_result
MDLparser = generate_parser()

logger = logging.getLogger(__name__)

class NotFoundError(Exception): pass

class ValidationState(object):
    """Object used in validation of types.
    
    Attributes:
        errors: List of error messages from validations.
        warnings: List of warnings from validations.
        valid: Boolean.
        indent: String representing the indentation level for output.
    """
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.valid = True
        self.indent = ""
        self.valid_cache = {}

    def add_error(self, msg):
        """Adds an error message to ValidationState's list of errors.
        
        Args:
            msg: An error string.
        """
        self.errors.append(self.indent + str(msg) + "\n")
        self.set_valid(False)

    def add_warning(self, msg):
        """Adds a warning message to ValidationState's list of warnings.
        
        Args:
            msg: An warning string.
        """
        self.warnings.append(self.indent + str(msg) + "\n")

    def set_valid(self, state):
        """Sets the validity of the ValidationState.
        
        Args:
            state: Boolean.
        """
        self.valid = bool(state)

    @contextlib.contextmanager
    def error_boundry(self, msg):
        """Adds a message to header future errors.
        
        Args:
            msg: An error message string.
        """
        old_valid = self.valid      # (1) Store old valid state
        self.add_error(msg)         # (2) Add the error boundary message preemptively
        self.indent += "\t"         # (3) Indent
        self.set_valid(True)        # Set valid True so we can test it later.
        try:
            yield
        except Exception as e:
            self.add_error("{}\n{}\--> And got exception: {}".format(msg, self.indent, e))
            raise
        finally:
            # If no errors are found, revoke the error message from earlier (2)
            if self.valid:
                self.errors = self.errors[:-1]

            # Restore valid state and index (1, 3)
            self.set_valid(old_valid)
            self.indent = self.indent[:-1]


class MDLDescription(object):
    """An object holding an MDLDescription.
            
    Attributes:
        ast: An AST Loader from loaders.py
        dependencies: Dictionary mapping PluginIds to MDLDescription objects.
    """

    def ast():
        doc = "The ast property."
        def fget(self):
            if self._ast is None:
                ast = self.ast_loader.load(self.dir)
                # clean up ast order
                self._ast = sorted(ast, key=self.keyfunc)
                self.validate()
            return self._ast
        def fset(self, v):
            self._ast = v
        return locals()
    ast = property(**ast())

    def __init__(self, ast_loader, dependencies, dir=""):
        self._ast = None
        self.dir = dir
        self.ast_loader = ast_loader
        self.dependencies = dependencies

    def copy(self):
        if not (self.ast is None):
            ast_loader = MdlRawLoader(list(self.ast))
        else:
            ast_loader = self.ast_loader
        return MDLDescription(ast_loader, dict(self.dependencies))

    @staticmethod
    def keyfunc(node):
        """Returns a key, node name pair depending on the type of node passed into the function.
        
        Args:
            node: The node to fetch a key, node pair
            
        Returns:
            (0, "") if the node is a Declaration.
            (1, node.name) if the node is a TypeFunction.
            (2, node.name) if the node is a TypePointer.
            (3, node.name) if the node is not any of the above types.
        """
        if isinstance(node, nodes.Declaration):
            return (0, "")
        else:
            if node.type.node_type() == base_types.TypeFunction:
                return (1, node.name)
            elif node.type.node_type() == base_types.TypePointer:
                return (2, node.name)
            else:
                return (3, node.name)

    @staticmethod
    def split_namespace(stringname):
        """Splits stringname into namespace, symbol pair.
        
        Args:
            stringname: fully qualified name of symbol.

        returns:
            (namespace, symbol) string pair.
        """
        split_name = stringname.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])
        return (namespace, end_name)

    def declarations(self):
        """Filters the root AST for nodes declaring new types or other information that aren't variables."""
        return list(filter(lambda n: isinstance(n, nodes.Declaration), self.ast))

    def definitions(self):
        """Filters the root AST for nodes defining new variables or other information that aren't declarations."""
        return list(filter(lambda n: isinstance(n, nodes.Definition), self.ast))

    def get_context(self, namespace):
        """Returns the MDLDescription object of the provided namespace.
        
        Args:
            namespace: A named string representing the namespace of the desired MDLDescription object.
            
        Returns:
            self if namespace is an empty string, and the MDLDescription object of the subnode within the current object otherwise.
        """
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
        """Returns true if the provided symbol is a valid symbol, false otherwise."""
        return not (cls._symbol_regex.search(symbol) is None)

    def _validate_roots(self, validation):
        """Validates the root nodes within the provided MDLDescription object.
        
        Args:
            validation: An MDLDescription object.
        """
        for node in self.ast:
            if not (isinstance(node, nodes.Declaration) or isinstance(node, nodes.Definition)):
                validation.add_warning("Root node {} is not declaration or definition.".format(node))

    def _validate_namespace(self, validation):
        """Validates the namespaces of each node within the provided MDLDescription object.
        
        Args:
            validation: An MDLDescription object.
        """
        namespaces = {}
        for node in self.ast:
            namespacekey = node.get_namespace_key()
            if not (namespacekey in namespaces):
                namespaces[namespacekey] = set()

            if node.name in namespaces[namespacekey]:
                validation.add_error("Duplicate name '{}' in namespace ({}).".format(node.name, namespacekey))

            namespaces[namespacekey].add(node.name)

    def _validate_ast(self, validation):
        """Validates the subnodes within the provided MDLDescription object.
        
        Args:
            validation: An MDLDescription object.
        """
        for node in self.ast:
            with validation.error_boundry("Node {} failed validation:".format(node)):
                node.validate(validation, self)

    def validate(self):
        """Checks for valid declarations.
        
        Returns:
            The validation state of the current object after checking for validation.
        """
        validate_state = ValidationState()

        # Do validation
        self._validate_roots(validate_state)
        self._validate_namespace(validate_state)
        self._validate_ast(validate_state)

        # Print messages:
        if validate_state.warnings:
            logger.warning("Validation Warnings:\n{}".format("".join(validate_state.warnings)))

        if validate_state.errors:
            logger.error("Validation Errors:\n{}".format("".join(validate_state.errors)))

        # Return
        return validate_state.valid

    @classmethod
    def map_over(cls, ast, map_func):
        """Applies a map function over this nodes subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
            ast: List of subnodes,
        
        Returns:
            The subnodes after having the map function applied to it.
        """
        new_ast = []
        for node in ast:
            new_subs = map_func(node)
            for new_sub_node in new_subs:
                new_ast.append(new_sub_node.map_over(map_func))
        return new_ast
