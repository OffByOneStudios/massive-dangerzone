"""MDL/base_types.py
@OffbyOne Studios
Base types of MDL. All wrappers should be able to work with these types.
"""

import logging

from .nodes import *

logger = logging.getLogger(__name__)

TypeType.Pointer = lambda s: TypePointer(s)

class TypeTypeSimple(TypeType):
    """A bare bones type."""
    def __eq__(self, other):
        return (self.__class__ == other.__class__)

    def __hash__(self):
        return hash(self.__class__)

    def copy(self):
        return self

    def node_type(self):
        return self


class TypeTypeNone(TypeTypeSimple):
    """Void type, meaning it has no return type"""

    def __repr__(self):
        return "TypeNone"

TypeNone = TypeTypeNone()


class TypeTypeWidth(TypeTypeSimple):
    """A Type which can have a width parameter.
    ie. Integers have a width parameter. Those widths commonly referred to as byte, short, int, long, etc

    Attributes:
        width : List of Integer Bit Width of type
    """
    _valid_widths = []

    def __init__(self, width):
        self.width = width
        if not self._valid():
            raise InvalidTypeMDLError("'{}' is not a valid width for a {}.".format(self.width, self.__class__))

    def _valid(self):
        """Private validator for TypeWidth objects.
        
        Returns:
            Boolean True iff instantiated width is within given width range, False otherwise.
        """
        return (self.width in self._valid_widths)

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.width == other.width

    def __hash__(self):
        return hash((self.__class__, self.width))

    def validate(self, validation, context):
        #TODO(Any): Make context do something
        """Validates TypeWidth objects to ensure their within is within their given range.
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        if not self._valid():
            validation.add_error("WidthType[{}] value {} is not valid.".format(self.__class__.__name__, self.width))


class TypeInt(TypeTypeWidth):
    """Type representing machine integers, and their various widths."""
    _valid_widths = [8, 16, 32, 64]

    def __repr__(self):
        return "TypeInt{}".format(self.width)

TypeInt8 = TypeInt(8)
TypeInt16 = TypeInt(16)
TypeInt32 = TypeInt(32)
TypeInt64 = TypeInt(64)

TypeChar = TypeInt(8)

class TypeUInt(TypeTypeWidth):
    """Type representing machine unsigned integers, and their various widths."""
    _valid_widths = [8, 16, 32, 64]

    def __repr__(self):
        return "TypeUInt{}".format(self.width)

TypeUInt8 = TypeUInt(8)
TypeUInt16 = TypeUInt(16)
TypeUInt32 = TypeUInt(32)
TypeUInt64 = TypeUInt(64)

class TypeFloat(TypeTypeWidth):
    """Type representing machine floating point values, and their various widths."""
    _valid_widths = [32, 64, 128, 256]

    def __repr__(self):
        return "TypeFloat{}".format(self.width)

TypeFloat32 = TypeFloat(32)
TypeFloat64 = TypeFloat(64)


class TypeTypeComplex(TypeType):
    """A type for complex objects."""
    def node_type(self):
        return self.__class__

class TypePointer(TypeTypeComplex):
    """A type representing a pointer to another type"""

    def __init__(self, type=None):
        """A type representing a pointer to another type

        Attributes:
            type: The type the pointer will point to.
        """
        self.type = type

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.type == other.type

    def __hash__(self):
        return hash((self.__class__, self.type))

    def __repr__(self):
        return "TypePointer({!r})".format(self.type)

    def copy(self):
        return self.__class__(type=None if self.type is None else self.type.copy())

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        TypeType.type_validate(validation, self.type, context)

    def map_over(self, map_func):
        """Applies a map function over this node and its new subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
        
        Returns:
            The node after having the map function applied to it.
        """
        return self.__class__(self._map_over_single_val(self, map_func, self.type))

class TypeArray(TypeTypeComplex):
    """Fixed length array of homogeneous components.

    Attributes:
        length: Number of elements
        type: Type of elements
    """
    def __init__(self, type, length):
        """Fixed length array of homogenous components.

        Args:
            type: Type of elements
            length: Number of elements
        """
        self.type = type
        self.length = length

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.type == other.type and self.length == other.length

    def __hash__(self):
        return hash((self.__class__, self.type, self.length))

    def __repr__(self):
        return "TypeArray({!r}, {!r})".format(self.type, self.length)

    def copy(self):
        return self.__class__(length=self.length, type=None if self.type is None else self.type.copy())

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        try:
            foo = int(self.length)
        except ValueError:
            validation.add_error("Array length is not an int.")
        TypeType.type_validate(validation, self.type, context)

    def map_over(self, map_func):
        """Applies a map function over this node and its new subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
        
        Returns:
            The node after having the map function applied to it.
        """
        return self.__class__(self._map_over_single_val(self, map_func, self.type), self.length)


class TypeStructElement(TypeTypeComplex):
    """Type for elements within structures.
    
    Attributes:
        name: String name of the type
        type: A TYpe object
    """
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type

    def is_general_type(self):
        return False

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.type == other.type and \
            self.name == other.name

    def __hash__(self):
        return hash((self.__class__, self.name, self.type))

    def __repr__(self):
        return "TypeStructMember({!r}, {!r})".format(self.name, self.type)

    def copy(self):
        return self.__class__(name=self.name, type=None if self.type is None else self.type.copy())

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        if not context.is_valid_symbol(self.name):
            validation.add_error("StructElement name '{}' is not valid.".format(self.name))

        TypeType.type_validate(validation, self.type, context)

    def map_over(self, map_func):
        """Applies a map function over this node and its new subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
        
        Returns:
            The node after having the map function applied to it.
        """
        return self.__class__(self.name, self._map_over_single_val(self, map_func, self.type))


class TypeStruct(TypeTypeComplex):
    """A fixed size record of heterogeneous components.

    Attributes:
        elements: Dictionary mapping names in the struct to types
    """

    def __init__(self, elements=[]):
        """A fixed size record of heterogeneous components.n

        Args:
            elements: Dictionary mapping names in the struct to types
        """
        elements = list(elements)

        self.elements = elements
        self._elements_hash = hash(tuple(elements))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.elements == other.elements

    def __hash__(self):
        return hash((self.__class__, self._elements_hash))

    def __repr__(self):
        return "TypeStruct({!r})".format(self.elements)

    def get_complex_list(self):
        return self.elements

    def copy(self):
        return self.__class__(elements=[v.copy() for v in self.elements])

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        if len(elements) == 0:
            validation.add_error("Structs must contain elements.")
            return
        for element in self.elements:
            with validation.error_boundry("Struct element not valid:"):
                if not (isinstance(element, TypeStructElement)):
                    validation.add_error("Not a TypeStructElement.")
                    return
                element.validate(validation, context)

    def map_over(self, map_func):
        """Applies a map function over this node and its new subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
        
        Returns:
            The node after having the map function applied to it.
        """
        new_elements = []
        for node in self.elements:
            new_subs = map_func(node)
            for new_sub_node in new_subs:
                new_elements.append(new_sub_node.map_over(map_func))
        return self.__class__(new_elements)


class TypeFunctionArgument(TypeTypeComplex):
    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type

    def is_general_type(self):
        return False

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.type == other.type and \
            self.name == other.name

    def __hash__(self):
        return hash((self.__class__, self.name, self.type))

    def __repr__(self):
        return "TypeFunctionArgument({!r}, {!r})".format(self.name, self.type)

    def copy(self):
        return self.__class__(name=self.name, type=None if self.type is None else self.type.copy())

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        if not context.is_valid_symbol(self.name):
            validation.add_error("StructElement name '{}' is not valid.".format(self.name))

        TypeType.type_validate(validation, self.type, context)

    def map_over(self, map_func):
        """Applies a map function over this node and its new subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
        
        Returns:
            The node after having the map function applied to it.
        """
        return self.__class__(self.name, self._map_over_single_val(self, map_func, self.type))


class TypeFunction(TypeTypeComplex):
    """A Function Type

    Attributes:
        return_type: Type object specifying the return type signiture of the function
        args: list of TypeFunctionArgument objects

    """
    def __init__(self, return_type = TypeNone, args=[]):
        self.return_type = return_type
        self.args = list(args)
        self._arg_lookup = dict((i[1].name, i[0]) for i in enumerate(args))
        self._ret_args_hash = hash((return_type, tuple(args)))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.return_type == other.return_type and \
            self.args == other.args

    def __hash__(self):
        return hash((self.__class__, self._ret_args_hash))

    def __repr__(self):
        return "TypeFunction({!r}, {!r})".format(self.return_type, self.args)

    def get_complex_list(self):
        return self.args

    def copy(self):
        return self.__class__(return_type=None if self.return_type is None else self.return_type.copy(), args=[v.copy() for v in self.args])

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        TypeType.type_validate(validation, self.return_type, context)

        for arg in self.args:
            with validation.error_boundry("Function argumen not valid:"):
                if not (isinstance(arg, TypeFunctionArgument)):
                    validation.add_error("Not a TypeFunctionArgument.")
                    return
                arg.validate(validation, context)

    def map_over(self, map_func):
        """Applies a map function over this node and its new subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
        
        Returns:
            The node after having the map function applied to it.
        """
        new_return_type = self._map_over_single_val(self, map_func, self.return_type)

        new_args = []
        for node in self.args:
            new_subs = map_func(node)
            for new_sub_node in new_subs:
                new_args.append(new_sub_node.map_over(map_func))
        return self.__class__(return_type=new_return_type, args=new_args)

    def get_arg(self, name):
        return self.args[self._arg_lookup[name]]


class NamedType(TypeTypeComplex):
    """A Variable associated with a Declared Type

    While builtin types are represented by their associated types above, declared types
    (Like TypeStructType) are associated with the string name of the declared type.


    Attributes:
        symbol: str name of declared type.
    """
    def __init__(self, symbol):
        """Struct Declaration constructor

        Args:
            symbol: string name of a type
        """
        self.symbol = symbol
        self._res_type = None

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.symbol == other.symbol

    def __hash__(self):
        return hash((self.__class__, self.symbol))

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.symbol)

    def copy(self):
        return self.__class__(symbol=self.symbol)

    class SymbolResolutionError(Exception): pass

    def resolve(self, context):
        """Sets the type of the node.
        
        Args:
            context: MdlDescription object
        """
        namespace, symbol = context.split_namespace(self.symbol)
        try:
            root_node = context.get_root_node(namespace, lambda n: isinstance(n, TypeDeclaration) and n.name == symbol)
        except:
            raise SymbolResolutionError("Symbol not found: {}".format(self.symbol))
        self._res_type = root_node.type

    def get_type(self):
        return self._res_type

    def validate(self, validation, context):
        """Validates this node and its subnodes in the given context
        
        Args:
            validation: ValidationState object
            context: MdlDescription object
        """
        # Add valid cach dictionary
        if not ("base_types.NamedType" in validation.valid_cache):
            validation.valid_cache["base_types.NamedType"] = set()

        # Attempt to resolve type
        try:
            self.resolve(context)
        except:
            validation.add_error("Exception when resolving NamedType")
            return

        # Check that it derives from TypeType.
        if not isinstance(self._res_type, TypeType):
            validation.add_error("NamedType result '{}' is not a Type.".format(self._res_type))
            return

        # Check that is is a general type.
        if not self._res_type.get_type().is_general_type():
            validation.add_error("Type {} is not a general type.".format(self._res_type))
            return

        # Validate the resolved type; only if validation hasn't already started.
        if not (self.symbol in validation.valid_cache["base_types.NamedType"]):
            with validation.error_boundry("Type {} is not valid.".format(self._res_type)):
                validation.valid_cache["base_types.NamedType"].add(self.symbol)
                self._res_type.validate(validation, context.get_context(context.split_namespace(self.symbol)[0]))

