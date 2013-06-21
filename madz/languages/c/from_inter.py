"""from_inter.py
@OffbyOne Studios
Converts from MDL to C headers
"""
import sys

sys.path.append("../../")
from pyMDL import *

function_prefix ="___madz_TYPE_"

class From_Inter(object):
    def make_typedefs(self, interface):
        namespace = interface.name.replace(".","__")
        res = ""
        functions = []
        for key,val in interface.declarations.items():
            if isinstance(val, TypeFunction):
                functions.append((key,val))
            elif isinstance(val, TypeTypedef):
                res+=self.as_c_statement(interface.name, key,val)+";\n"
            elif isinstance(val,TypeStructType):
                res += self.as_c_statement(interface.name,key,val) + ";\n"
        for key,val in functions:
            arglist = [self.as_c_statement(interface.name,"",v) for k,v in val.args.items()]
            args= "("
            for i in arglist:
                args += i + ", "

            args=args[0:len(args)-3] + ")"
            res += "typedef "+ self.as_c_statement(interface.name,"",val.return_type) + "(*" +function_prefix + namespace + "_"+ key +")" + args + ";\n"



        return res

    def make_structs(self, interface):
        namespace = interface.name.replace(".","__")
        res = "typedef struct{\n"
        for key,val in interface.declarations.items():
            if isinstance(val,TypeFunction):
                res += "\t"+function_prefix +key+ " "+key +";\n";
            elif not isinstance(val,TypeStructType) and not isinstance(val,TypeTypedef):
                res += "\t"+self.as_c_statement(interface.name, key, val)+";\n"
        res += '}' + function_prefix+namespace + ";"
        return res;

    def as_c_statement(self,name, key, val):
        namespace = name.replace(".","__")
        def table_struct(key):
            s = "typedef struct{\n"
            for k,v in val.value.items():
                s += "\t" + self.as_c_statement(name,k,v) + ";\n"
            s += "} " + function_prefix+namespace+"_" +key
            return s
        def table_function(key):
            ret = self.as_c_statement(name, "", val.return_type)
            ret += key + "("
            for k, v in val.args.items():
                ret += self.as_c_statement(k,v) + ", "
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
            TypeTypedef : lambda k: "typedef " + self.as_c_statement(name, "",val.type) + function_prefix+namespace+"_"+key,
            TypeStructVar : lambda k: "struct " + function_prefix+namespace + "_"+val.value + " " + key,
            TypePtr : lambda k: self.as_c_statement(name, "",val.value) + "*" + key,
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


def main():
    sys.path.append("../../../examples/simple_interface_example/Barks/module/interface")
    sys.path.append("../../../")
    import imodule
    f = From_Inter()
    p = imodule.plugin
    #res = convert(p)

    tdefs = f.make_typedefs(p)
    print tdefs
    structs= f.make_structs(p)
    print structs
if __name__ =='__main__':
    main()


