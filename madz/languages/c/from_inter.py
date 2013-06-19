"""from_inter.py
@OffbyOne Studios
Converts from MDL to C headers
"""
import sys

sys.path.append("../../../")
from pyMDL import *

def as_c_statement(key,val):
    if isinstance(val, TypeNone):
        return "void "
    if isinstance(val, TypeVoid):
        return "void " + key
    if isinstance(val, TypeInt8):
        return "char " + key
    if isinstance(val, TypeInt16):
        return "short " + key
    if isinstance(val, TypeInt32):
        return "int " + key
    if isinstance(val, TypeInt64):
        return "long long " + key
    if isinstance(val, TypeUInt8):
        return "unsigned char " + key
    if isinstance(val, TypeUInt16):
        return "unsigned short " + key 
    if isinstance(val, TypeUInt32):
        return "unsigned int " + key
    if isinstance(val, TypeInt64):
        return "unsigned long long" + key
    if isinstance(val, TypeFloat32):
        return "float "+ key
    if isinstance(val, TypeFloat64):
        return "double " + key
    if isinstance(val, TypeChar):
        return "char " + key
    if isinstance(val, TypeTypedef):
        return "typedef " +as_c_statement("",val.type) + key
    if isinstance(val, TypeStructType):
        s= "typedef struct{\n"
        for k,v in val.value.items():
            s+="\t"+as_c_statement(k,v)+";\n"
            #s+="\t"+as_c_statement(k,v)+";\n"
        s+="}"+key
        return s
    if isinstance(val, TypeStructVar):
        return "struct "+val.value+" "+key
    if isinstance(val, TypePtr):
        return as_c_statement("",val.value)+"*"+ key
    if isinstance(val, TypeFunction):
        ret = as_c_statement("", val.return_type)
        ret += key +"("
        for k,v in val.args.items():
            ret+=as_c_statement(k,v)+", "
        ret = ret[0:len(ret)-2]+")"
        return ret

    else:
        print type(val)
        raise NotImplementedError


def convert(interface):
    """Converts interface's contents to C header/body file

    Args:
        a MDL interface object
    Returns:
        String representing source and header file
    """
    head = "/*" + interface.name + ".h\nVersion:" + interface.version + "\n" + "*/\n"
    statements=[]
    for key,val in interface.declarations.items():
        statements.append(as_c_statement(key,val))

    res=""
    print "Dyst@"
    #print statements
    for i in statements:
        print i
    return res


def main():
    sys.path.append("../../../examples/simple_interface_example/Barks/module/interface")
    sys.path.append("../../../")
    import imodule

    p = imodule.plugin
    res = convert(p)
    print res
if __name__ =='__main__':
    main()
    

