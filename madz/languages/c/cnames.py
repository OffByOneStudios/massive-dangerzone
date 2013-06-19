
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
    pass


class TypeInt16(Type):
    pass


class TypeInt32(Type):
    pass


class TypeInt64(Type):
    pass


class TypeUInt8(Type):
    pass


class TypeUInt16(Type):
    pass


class TypeUInt32(Type):
    pass


class TypeInt64(Type):
    pass


class TypeFloat32(Type):
    pass


class TypeFloat64(Type):
    pass


class TypeChar(Type):
    pass

class TypeTypedef(Type):
    """A Typedef"""
    def __init(self, the_type):
        """Typedef Type constructor
        Args:
            type :The Type to alias
        """
        self.type = the_type


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
    def __init__(self, value):
        """C Pointer Representation

        Args:
            value:
                A Type, potentially initialized.
        """

class TypeFunction(Type):

    def __init__(self, return_type = ITNone(), args={}, attributes = []):
        self.return_type = return_type
        self.attributes = attributes
        self.args = args
        
    
