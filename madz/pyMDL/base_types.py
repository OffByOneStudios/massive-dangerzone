"""interface.py
@OffbyOne Studios
Base types of MDL. Everything should be able to work with this.
"""

from nodes import *

TypeType.Pointer = lambda s: TypePointer(s)

class TypeTypeSimple(TypeType):
    def __eq__(self, other):
        return (self.__class__ == other.__class__)

    def __hash__(self):
        return hash(self.__class__)

    def node_type(self):
        return self


class TypeTypeNone(TypeTypeSimple):
    """Void, as in No Return Type"""
    pass

TypeNone = TypeTypeNone()


class TypeTypeWidth(TypeTypeSimple):
    """A Type which can have a width parameter.
    ie. Integers have a width parameter. Those widths commonly refered to as byte, short, int, long, etc

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
            Boolean True iff instantiated width is with given width range, False otherwise.
        """
        return (self.width in self._valid_widths)

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.width == other.width

    def __hash__(self):
        return hash((self.__class__, self.width))

    def validate(self, context):
        return self._valid()


class TypeInt(TypeTypeWidth):
    """Object Representing Machine Integers, and their varius widths."""
    _valid_widths = [8, 16, 32, 64]

TypeInt8 = TypeInt(8)
TypeInt16 = TypeInt(16)
TypeInt32 = TypeInt(32)
TypeInt64 = TypeInt(64)

class TypeUInt(TypeTypeWidth):
    """Object Representing Machine Unsigned Integers, and their varius widths."""
    _valid_widths = [8, 16, 32, 64]

TypeUInt8 = TypeUInt(8)
TypeUInt16 = TypeUInt(16)
TypeUInt32 = TypeUInt(32)
TypeUInt64 = TypeUInt(64)

TypeChar = TypeUInt(8)

class TypeFloat(TypeTypeWidth):
    """Object Representing Machine Floating Point Values, and their varius widths."""
    _valid_widths = [32, 64, 128, 256]

TypeFloat32 = TypeFloat(32)
TypeFloat64 = TypeFloat(64)


class TypeTypeComplex(TypeType):
    def node_type(self):
        return self.__class__

class TypePointer(TypeTypeComplex):
    """A type representing a pointer to another type"""

    def __init__(self, type):
        """A type representing a pointer to another type

        Agttributes:
            type: The type the pointer will point to.
        """
        self.type = type
        self._valid()

    _invalid_subtypes = []

    def _valid(self):
        if len(filter(lambda l: isinstance(self.type, l), self._valid_subtypes)) != 0:
            raise InvalidTypeMDLError("Pointer Cannot Point to Type: {}".format(self.type))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.type == other.type

    def __hash__(self):
        return hash((self.__class__, self.type))

    def validate(self, context):
        return TypeType.type_validate(self.type, context)

    def map_over(self, map_func):
        return self.__class__(self._map_over_single_val(self, map_func, self.type))

class TypeArray(TypeTypeComplex):
    """Fixed length array of homogenous components.

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

    def validate(self, context):
        try:
            foo = int(self.length)
        except ValueError:
            return False
        return TypeType.type_validate(self.type, context)

    def map_over(self, map_func):
        return self.__class__(self._map_over_single_val(self, map_func, self.type), length)


class TypeStruct(TypeTypeComplex):
    """A fixed size record of hetrogenous components.

    Attributes:
        elements: Dictionary mapping names in the struct to types

    """

    def __init__(self, elements):
        """A fixed size record of hetrogenous components.n

        Args:
            elements: Dictionary mapping names in the struct to types
        """
        self.elements = elements
        self._elements_hash = hash(tuple(sorted(elements.iteritems())))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.elements == other.elements

    def __hash__(self):
        return hash((self.__class__, self._elements_hash))

    def validate(self, context):
        for key, val in self.elements.items():
            if not (context.is_valid_symbol(key) and TypeType.type_validate(val, context)):
                return False
        return True

    def map_over(self, map_func):
        new_elements = {}
        for name, node in self.elements.iteritems():
            new_subs = map_func(node, name=name)
            for new_sub_name, new_sub_node in new_subs:
                if new_sub_name in new_elements:
                    raise InvalidTypeMDLError("Struct can not have multiple new elements with the same name: {}".format(new_sub_name))
                new_elements[new_sub_name] = new_sub_node.map_over(map_func)
        return self.__class__(new_elements)


class TypeFunctionArgument(TypeTypeComplex):
    def __init__(self, name, type):
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

    def validate(self, context):
        return context.is_valid_symbol(self.name) and TypeType.type_validate(self.type, context)

    def map_over(self, map_func):
        return self.__class__(self.name, self._map_over_single_val(self, map_func, self.type))


class TypeFunction(TypeTypeComplex):
    """A Function Type

    Attributes:
        return_type: Type object specifying the return type signiture of the function
        args: Dict of (str,Type) tuples representing function arguements

    """
    def __init__(self, return_type = TypeNone, args=[]):
        self.return_type = return_type
        self.args = args
        self._arg_lookup = dict((i[1].name, i[0]) for i in enumerate(args))
        self._ret_args_hash = hash((return_type, tuple(args)))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.return_type == other.return_type and \
            self.args == other.args

    def __hash__(self):
        return hash((self.__class__, self._ret_args_hash))

    def validate(self, context):
        if not TypeType.type_validate(self.return_type, context):
            return False

        for arg in self.args:
            if not (
                isinstance(arg, TypeFunctionArgument) and \
                arg.validate(context)):
                return False

        return True

    def map_over(self, map_func):
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

    def resolve(self, context):
        namespace, symbol = context.split_namespace(self.symbol)
        self._res_type = context.get_root_node(namespace, lambda n: isinstance(n, TypeDeclaration) and n.name == symbol).type

    def get_type(self):
        return self._res_type

    def validate(self, context):
        self.resolve(context)

        return TypeType.type_validate(self._res_type,
            context.get_context(context.split_namespace(self.symbol)[0]))

