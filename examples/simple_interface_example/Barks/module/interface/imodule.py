import sys
sys.path.append("../../../../../")
from pyMDL import *
                
plugin = Plugin(name = "Barks.module",
    version = "0.0.1",
    requires = [],
    declarations = {
        #Type Declarations
        "month":ITTypedef(ITInt8()),
        "Point2d":ITStructType({
        "x":ITInt32(),
        "y":ITInt32(),
        }),
        #Variable Declarations
        "var1":ITInt8(), #A Byte, uninitialized
        "var2":ITInt16(8), #A Short, initiailized
        "var3":ITPtr(ITChar()),#A Char Pointer, Unintialized
        "apoint":ITStructVar("Point2d"),
        #Functions
        "do_foo":ITFunction(
            return_type = ITNone(),
            args = {"i":ITInt32()}
            ),
        "do_obj_foo":ITFunction(
            ITNone(),
            
            {"theFoo":ITPtr(ITStructVar("Point2d")),"j":ITInt32()}),
        
        "set_foo":ITFunction(
            ITInt32(),
            {
                "foo":ITPtr(ITVoid()),
                "j":ITInt32()
                }
            )
    }


)

