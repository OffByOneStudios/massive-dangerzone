"""from_inter.py
@OffbyOne Studios
Converts from MDL to C headers
"""
import sys

sys.path.append("../../../")
from pyMDL import *

def as_c_statement(key, val):
    def table_struct(key):
        s = "typedef struct{\n"
        for k,v in val.value.items():
            s += "\t" + as_c_statement(k,v) + ";\n"
        s += "} " + key
        return s
    def table_function(key):
        ret = as_c_statement("", val.return_type)
        ret += key + "("
        for k, v in val.args.items():
            ret += as_c_statement(k,v) + ", "
        ret = ret[0:len(ret)-2] + ")"
        return ret

    table = {
        TypeNone : lambda k: "void ",
        TypeVoid : lambda k: "void " + k,
        TypeInt8 : lambda k: "char " + k,
        TypeInt16 : lambda k: "short " + k,
        TypeInt32 : lambda k: "int " + k,
        TypeInt64 : lambda k: "long long " + k,
        TypeUInt8 : lambda k: "unsigned char " + k,
        TypeUInt16 : lambda k: "unsigned short " + k,
        TypeUInt32 : lambda k: "unsigned int " + k,
        TypeInt64 : lambda k: "unsigned long long" + k,
        TypeFloat32 : lambda k: "float "+ k,
        TypeFloat64 : lambda k: "double " + k,
        TypeChar : lambda k: "char " + k,
        TypeTypedef : lambda k: "typedef " + as_c_statement("",val.type) + k,
        TypeStructVar : lambda k: "struct " + val.value + " " + key,
        TypePtr : lambda k: as_c_statement("",val.value) + "*" + key,
        TypeStructType : table_struct,
        TypeFunction : table_function
    }

    return table[val.__class__](key)

def ordering(node):
    node_type = node[0].__class__
    # Typedefs
    # Structs
    # Variables
    # Fucntions
    if node_type == TypeTypedef:
        return 1
    elif node_type == TypeStructType:
        return 2
    elif node_type == TypeFunction:
        return 4
    else:
        return 3

def convert(interface):
    """Converts interface's contents to C header/body file

    Args:
        a MDL interface object
    Returns:
        String representing source and header file
    """
    res=""
    head = "/*" + interface.name + ".h\nVersion:" + interface.version + "\n" + "*/\n"
    statements = map(lambda node: (node[1], as_c_statement(node[0], node[1])), interface.declarations.items())
    statements = sorted(statements, key=ordering)
    for i in statements:
        res+= i[1] + ";\n"

    return head+res


def main():
    sys.path.append("../../../examples/simple_interface_example/Barks/module/interface")
    sys.path.append("../../../")
    import imodule

    p = imodule.plugin
    res = convert(p)
    print res
if __name__ =='__main__':
    main()
    

