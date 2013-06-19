"""from_inter.py
@OffbyOne Studios
Converts from MDL to C headers
"""
import sys

sys.path.append("../../../")
from pyMDL import *



def _get_typedefs(s):
    res = ""
    for key,val in s.items():
        if isinstance(val,ITTypedef):
            res+="typedef "
            
        
def _get_structs(s):
    """Convert structs into source code"""
    pass


def convert(interface):
    """Converts interface's contents to C header/body file

    Args:
        a MDL interface object
    Returns:
        String representing source and header file
    """
    head = "/*" + interface.name + ".h\nVersion:" + interface.version + "\n" + "*/\n"
    typedefs = _get_typedefs(interface.declarations)
    #print head





def main():
    sys.path.append("../../../examples/simple_interface_example/Barks/module/interface")
    sys.path.append("../../../")
    import imodule

    p = imodule.plugin
    convert(p)

if __name__ =='__main__':
    main()
    

