"""interface.py
@OffbyOne Studios
Basic Classes for C interportability
"""
from abc import ABCMeta

class Interface_Type(object):
    """Abstract Base Class for Types"""
    __metaclass__ = ABCMeta

    def __init__(self, value=None):
        self.value = value

        
class ITNone(Interface_Type):
    """Void, as in No Return Type"""
    pass


class ITVoid(Interface_Type):
    """Void, as in untyped (void *)"""
    pass


class ITInt8(Interface_Type):
    pass


class ITInt16(Interface_Type):
    pass


class ITInt32(Interface_Type):
    pass


class ITInt64(Interface_Type):
    pass


class ITUInt8(Interface_Type):
    pass


class ITUInt16(Interface_Type):
    pass


class ITUInt32(Interface_Type):
    pass


class UInt64(Interface_Type):
    pass


class ITFloat32(Interface_Type):
    pass


class ITFloat64(Interface_Type):
    pass


class ITChar(Interface_Type):
    pass

class ITTypedef(Interface_Type):
    """A Typedef"""
    def __init(self, the_type):
        """Typedef Type constructor
        Args:
            type :The Type to alias
        """
        self.type = the_type


class ITStructType(Interface_Type):
    """A Struct Declaration"""
    
    def __init__(self, value):
        """C Struct Representation
        Args:
            values:
                Dict of name,type pairs
        """
        self.value = value

class ITStructVar(Interface_Type):
    """A Struct Variable"""
    def __init__(self, value):
        """Struct Declaration constructor
        Args:
            value: string name of structtype
        """
        self.value = value


class ITPtr(Interface_Type):
    def __init__(self, value):
        """C Pointer Representation

        Args:
            value:
                A Type, potentially initialized.
        """

class ITFunction(Interface_Type):

    def __init__(self, return_type = ITNone(), args={}, attributes = []):
        self.return_type = return_type
        self.attributes = attributes
        self.args = args
        
    
