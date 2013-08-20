"""MDL/py_ctypes_gen.py
@OffbyOne Studios 2013
Turns MDL into python ctypes information.
"""
import ctypes

from . import *

def set_ctypes_from_mdl(ctypes_function, mdl):
    type_convert = {
        TypeNone : None,
    }
    args = [type_convert[mdl.return_type]] + list(map(lambda arg: type_convert[arg.type], mdl.args))
    return ctypes.CFUNCTYPE(*args)(ctypes_function)
