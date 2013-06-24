"""interface.py
@OffbyOne Studios
Basic Classes for C interportability
"""

class MDLError(Exception): pass
class InvalidTypeMDLError(MDLError): pass

class TypeType(object):
    """Abstract Base Class for Types"""
    def __init__(self): raise NotImplementedError()

    def __eq__(self, other):
        return (self.__class__ == other.__class__)

    def __hash__(self):
        return hash(self.__class__)

    def node_type(self):
        return self.__class__

    def Pointer(self):
        return TypePointer(self)

class TypeTypeNone(TypeType):
    """Void, as in No Return Type"""
    def __init__(self): pass

TypeNone = TypeTypeNone()

class TypeTypeWidth(TypeType):
    """A Type which can have a width parameter.
    ie. Integers have a width parameter. Those widths commonly refered to as byte, short, int, long, etc

    Attributes:
        width : List of Integer Bit Width of type
    """
    _valid_widths = []

    def __init__(self, width):
        self.width = width
        self._valid()

    def _valid(self):
        """Validator for TypeWidth objects.
        Returns:
            Boolean True iff instantiated width is with given width range, False otherwise.
        """

        if not (self.width in self._valid_widths):
            raise InvalidTypeMDLError("'{}' is not a valid width for a {}.".format(self.width, self.__class__))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.width == other.width

    def __hash__(self):
        return hash((self.__class__, self.width))

    def node_type(self):
        return self

class TypeInt(TypeTypeWidth):
    """Object Representing Machine Integers, and their varius widths."""
    _valid_widths = [8, 16, 32, 64]

TypeInt8 = TypeInt(8)
TypeInt16 = TypeInt(16)
TypeInt32 = TypeInt(32)
TypeInt64 = TypeInt(64)

TypeChar = TypeInt(8)

class TypeUInt(TypeTypeWidth):
    """Object Representing Machine Unsigned Integers, and their varius widths."""
    _valid_widths = [8, 16, 32, 64]

TypeUInt8 = TypeUInt(8)
TypeUInt16 = TypeUInt(16)
TypeUInt32 = TypeUInt(32)
TypeUInt64 = TypeUInt(64)

class TypeFloat(TypeTypeWidth):
    """Object Representing Machine Floating Point Values, and their varius widths."""
    _valid_widths = [32, 64, 128, 256]

TypeFloat32 = TypeFloat(32)
TypeFloat64 = TypeFloat(64)


class TypeTypedef(TypeType):
    """A C-StyleTypedef

    Attributes:
        type: The Type being aliased.
    """
    def __init__(self, t):
        """Typedef Type constructor

        Args:
            t: The Type to alias.
        """
        self.type = t

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.t == other.t

    def __hash__(self):
        return hash((self.__class__, self.t))


class TypePointer(TypeType):
    """A Pointer Type encapsulating another Type"""
    def __init__(self, t):
        """Pointer Type constructor

        Agttributes:
            t: The Type to be a pointer of.
        """
        self.type = t

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.t == other.t

    def __hash__(self):
        return hash((self.__class__, self.t))


class TypeArray(TypeType):
    """C Style Array Type.
    Attributes:
        count: Integer Count of number of elements
        type: Type of Array Element
    """
    def __init__(self, t, count):
        """Pointer Type constructor

        Args:
            t: The Type to be a pointer of.
            count: number of type t.
        """
        self.type = t
        self.count = count

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.t == other.t and self.count == other.count

    def __hash__(self):
        return hash((self.__class__, self.t, self.count))


class TypeStructType(TypeType):
    """A Record (C Struct) Type Declaration.

    Attributes:
        description: Dictionary of (str,Type) tuples

    """

    def __init__(self, desc):
        """C Struct Representation

        Args:
            desc:
                Dict of (name, type) pairs
        """
        self.description = desc
        self._desc_hash = hash(tuple(sorted(desc.iteritems())))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.description == other.description

    def __hash__(self):
        return hash((self.__class__, self._desc_hash))


class NamedType(TypeType):
    """A Variable associated with a Declared Type

    While builtin types are represented by their associated types above, declared types
    (Like TypeStructType) are associated with the string name of the declared type.


    Attributes:
        type: str name of declared type.
    """
    def __init__(self, t):
        """Struct Declaration constructor

        Args:
            t: string name of structtype
        """
        self.type = t

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.value == other.value

    def __hash__(self):
        return hash((self.__class__, self.value))


class TypeFunction(TypeType):
    """A Function Type

    Attributes:
        return_type: Type object specifying the return type signiture of the function
        args: Dict of (str,Type) tuples representing function arguements
        attributes: keyword modifiers of function (like extern/inline/public/etc..)

    """
    def __init__(self, return_type = TypeNone, args={}, attributes = []):
        self.return_type = return_type
        self.attributes = attributes
        self.args = args
