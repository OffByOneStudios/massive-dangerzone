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

    """
    _valid_widths = []

    def __init__(self, width):
        self.width = width
        self._valid()

    def _valid(self):
        if not (self.width in self._valid_widths):
            raise InvalidTypeMDLError("'{}' is not a valid width for a {}.".format(self.width, self.__class__))

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.width == other.width

    def __hash__(self):
        return hash((self.__class__, self.width))

    def node_type(self):
        return self

class TypeInt(TypeTypeWidth):
    _valid_widths = [8, 16, 32, 64]

TypeInt8 = TypeInt(8)
TypeInt16 = TypeInt(16)
TypeInt32 = TypeInt(32)
TypeInt64 = TypeInt(64)

TypeChar = TypeInt(8)

class TypeUInt(TypeTypeWidth):
    _valid_widths = [8, 16, 32, 64]

TypeUInt8 = TypeUInt(8)
TypeUInt16 = TypeUInt(16)
TypeUInt32 = TypeUInt(32)
TypeUInt64 = TypeUInt(64)

class TypeFloat(TypeTypeWidth):
    _valid_widths = [32, 64, 128, 256]

TypeFloat32 = TypeFloat(32)
TypeFloat64 = TypeFloat(64)


class TypeTypedef(TypeType):
    """A Typedef"""
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

        Args:
            t: The Type to be a pointer of.
        """
        self.type = t

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and self.t == other.t

    def __hash__(self):
        return hash((self.__class__, self.t))


class TypeArray(TypeType):
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
    """A Struct Declaration"""

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
    """A type which has bee previously declared.

    This is  oppsed to 'builtin' types, like integer.
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
    """A Function Type"""
    def __init__(self, return_type = TypeNone, args={}, attributes = []):
        self.return_type = return_type
        self.attributes = attributes
        self.args = args
