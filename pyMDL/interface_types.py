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


class ITStruct(Interface_Type):
    pass


class ITPtr(Interface_Type):
    pass


class ITNone(Interface_Type):
    pass


class ITFunction(Interface_Type):
    pass
    
