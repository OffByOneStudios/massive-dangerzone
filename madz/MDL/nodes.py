"""MDL/nodes.py
@OffbyOne Studios
Base nodes of MDL. All MDL manipulations should work with these. All extensions should be built off of a node listed here.
"""

import abc

class MDLError(Exception): pass
class InvalidTypeMDLError(MDLError): pass
class SyntaxMDLError(MDLError): pass
class MapOverMDLError: pass

class BaseNode(object):
    "Base node type."

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __hash__(self):
        pass

    @abc.abstractmethod
    def node_type(self):
        """Returns the type of the node, for dispatch."""
        pass

    @abc.abstractmethod
    def validate(self, validation, context):
        """Validates the AST tree from this point on."""
        pass

    @abc.abstractmethod
    def map_over(self, map_func):
        """Operates on each member of the AST."""
        pass

    def is_extension(self):
        return False

    def is_attribute(self):
        return False

    @staticmethod
    def _map_over_single_val(self, map_func, val):
        new_sub = map_func(val)
        if len(new_sub) != 1:
            raise MapOverMDLError("Single val expected. Got instead: {}".format(new_sub))
        return new_sub[0].map_over(map_func)

class Node(BaseNode):
    def get_attribute(self, type):
        if hasattr(self, "attributes"):
            return self.attributes.get(type, None)
        return None

    def set_attribute(self, type, value):
        if not hasattr(self, "attributes"):
            self.attributes = {}
        self.attributes[type] = value

    def validate_attributes(self, validation, context):
        if not hasattr(self, "attributes"):
            return
        with validation.error_boundry("Attribute Validation Failed:"):
            for attr in self.attributes.items():
                attr.validate(validation, context)


class Attribute(BaseNode):
    def is_attribute(self):
        return True

    def on_attach(self, node):
        node.set_attribute(self.get_attr_type(), self)

    def get_attr_type(self):
        self.__class__

    def __call__(self, node):
        if (not isinstance(node, BaseNode)) and (not node.is_attribute()):
            raise ValueError("Must be decorated on a node")
        self.on_attach(node)
        return node


class DocumentationAttribute(Attribute):
    def __init__(self, documentation):
        self.documentation = documentation
    


class TypeType(Node):
    """Type base class."""
    def validate(self, validation, context):
        pass

    def map_over(self, map_func):
        return self

    def is_general_type(self):
        return True

    def is_namedonly_type(self):
        return False

    def get_type(self):
        return self

    @classmethod
    def type_validate(cls, validation, type, context, namedonly_ok=False):
        #validate should ensure that get_type behaves correctly
        if not (isinstance(type, TypeType)):
            validation.add_error("Node not of TypeType, type_validate failed.")
            return 

        with validation.error_boundry("Type {} is not valid:".format(type)):
            type.validate(validation, context)
        if not validation.valid:
            return

        if not type.get_type().is_general_type():
            validation.add_error("Type {} is not a general type.".format(type))
            return
        
        if not (namedonly_ok or not(type.get_type().is_namedonly_type())):
            validation.add_error("Type {} is a namedonly type.".format(type))
            return

        if not isinstance(type.get_type(), cls):
            validation.add_error("Type {} is not an instance of type {}.".format(type, cls.__name__))
            return

class RootNode(Node):
    @abc.abstractmethod
    def get_namespace_key(self):
        pass

    def node_type(self):
        """Returns the type of the node, for dispatch."""
        return self.__class__

class Declaration(RootNode):
    """A declaration of abstract information, as opposed to a definition."""
    pass

class TypeDeclaration(Declaration):
    """A declaration of a new type."""
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.name == other.name and \
            self.type == other.type

    def __hash__(self):
        return hash((self.__class__, self.name, self.type))

    def __repr__(self):
        return "TypeDeclaration({!r}, {!r})".format(self.name, self.type)

    def validate(self, validation, context):
        if not context.is_valid_symbol(self.name):
            validation.add_error("TypeDeclaration name '{}' is not a valid name.".format(self.name))
            return

        with validation.error_boundry("TypeDeclaration type '{}' is not valid:".format(self.type)):
            TypeType.type_validate(validation, self.type, context, namedonly_ok=True)

    def map_over(self, map_func):
        return self.__class__(self.name, self._map_over_single_val(self, map_func, self.type))

    class NamespaceKey(object): pass

    def get_namespace_key(self):
        return self.NamespaceKey

class Definition(RootNode):
    """A definition of concrete information, as opposed to a declaration."""
    pass

class VariableDefinition(Definition):
    """A definition of a new variables."""
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.name == other.name and \
            self.type == other.type

    def __hash__(self):
        return hash((self.__class__, self.name, self.type))

    def __repr__(self):
        return "TypeDeclaration({!r}, {!r})".format(self.name, self.type)

    def validate(self, validation, context):
        if not context.is_valid_symbol(self.name):
            validation.add_error("VariableDefinition name '{}' is not a valid name.".format(self.name))
            return

        with validation.error_boundry("VariableDefinition type '{}' is not valid:".format(self.type)):
            TypeType.type_validate(validation, self.type, context)

    def map_over(self, map_func):
        return self.__class__(self.name, self._map_over_single_val(self, map_func, self.type))

    class NamespaceKey(object): pass

    def get_namespace_key(self):
        return self.NamespaceKey

