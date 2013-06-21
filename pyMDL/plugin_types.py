"""interface.py
@OffbyOne Studios
Basic Classes for C interportability
"""
from abc import ABCMeta


class Type(object):
    """Abstract Base Class for Types"""
    __metaclass__ = ABCMeta

    def __init__(self, value=None):
        self.value = value


class TypeNone(Type):
    """Void, as in No Return Type"""
    pass


class TypeVoid(Type):
    """Void, as in untyped (void *)"""
    pass


class TypeInt8(Type):
    """8 Bit Signed Integer"""
    pass


class TypeInt16(Type):
    """16 Bit Signed Integer"""
    pass


class TypeInt32(Type):
    """32 Bit Signed Integer"""
    pass


class TypeInt64(Type):
    """64 Bit Signed Integer"""
    pass


class TypeUInt8(Type):
    """8 Bit Unsigned Integer"""
    pass


class TypeUInt16(Type):
    """16 Bit Unsigned Integer"""
    pass


class TypeUInt32(Type):
    """32 Bit Unsigned Integer"""
    pass


class TypeInt64(Type):
    """64 Bit Unsigned Integer"""
    pass


class TypeFloat32(Type):
    """32 Bit Floating Point Value"""
    pass


class TypeFloat64(Type):
    """64 Bit Floating Point Value"""
    pass


class TypeChar(Type):
    """8 Bit Latin_1 Character"""
    pass

class TypeTypedef(Type):
    """A Typedef"""
    def __init__(self, t):
        """Typedef Type constructor
        Args:
            type :The Type to alias
        """
        self.type = t


class TypeStructType(Type):
    """A Struct Declaration"""

    def __init__(self, value):
        """C Struct Representation
        Args:
            values:
                Dict of name,type pairs
        """
        self.value = value

class TypeStructVar(Type):
    """A Struct Variable"""
    def __init__(self, value):
        """Struct Declaration constructor
        Args:
            value: string name of structtype
        """
        self.value = value


class TypePtr(Type):
    """A Mutable Pointer"""
    pass
class TypeFunction(Type):
    """A Function"""
    def __init__(self, return_type = TypeNone(), args={}, attributes = []):
        self.return_type = return_type
        self.attributes = attributes
        self.args = args


