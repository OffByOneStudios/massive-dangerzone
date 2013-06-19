import sys
sys.path.append("../../../../../")
from pyMDL import *
                
plugin = Plugin(name = "Barks.module",
    version = "0.0.1",
    requires = [],
    declarations = {
        #Type Declarations
        "month":TypeTypedef(TypeInt8()),
        "Point2d":TypeStructType({
        "x":TypeInt32(),
        "y":TypeInt32(),
        }),
        #Variable Declarations
        "var1":TypeInt8(), #A Byte, uninitialized
        "var2":TypeInt16(8), #A Short, initiailized
        "var3":TypePtr(TypeChar()),#A Char Pointer, Unintialized
        "apoint":TypeStructVar("Point2d"),
        #Functions
        "do_foo":TypeFunction(
            return_type = TypeNone(),
            args = {"i":TypeInt32()}
            ),
        "do_obj_foo":TypeFunction(
            TypeNone(),
            
            {"theFoo":TypePtr(TypeStructVar("Point2d")),"j":TypeInt32()}),
        
        "set_foo":TypeFunction(
            TypeInt32(),
            {
                "foo":TypePtr(TypeVoid()),
                "j":TypeInt32()
                }
            )
    }


)

