from ... import nodes
from ... import base_types

extension_prefix = "MADZ_EXT_OBJECTS_"

class MemberFunctionDefinition(nodes.Definition):
    """Instance method object to be attached to classes.
    
    Attributes:
        name: String name of the function.
        type:
    """
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and \
            self.name == other.name and \
            self.type == other.type

    def __hash__(self):
        return hash((self.__class__, self.name, self.type))

    def validate(self, context):
        # TODO(Mason): Self parameter?
        return context.is_valid_symbol(self.name) and base_types.TypeFunction.type_validate(self.type, context)

    def map_over(self, map_func):
        return self.__class__(self.name, self._map_over_single_val(self, map_func, self.type))

    class NamespaceKey(object): pass

    def get_namespace_key(self):
        return self.NamespaceKey


class TypeClass(base_types.TypeTypeComplex):
    def __init__(self, parents=[], members=[]):
        self.parents = parents
        self.members = members
        self._hash = hash((hash(tuple(sorted(members, key=lambda n: (hash(n.__class__), n.name)))),
                          hash(tuple(parents))))
        self._type_dict = dict(\
            map(lambda m: (m.name, m.type), 
                filter(lambda m: isinstance(m, nodes.TypeDeclaration), self.members)))
        self._var_dict = dict(\
            map(lambda m: (m.name, m.type), 
                filter(lambda m: isinstance(m, nodes.VariableDefinition), self.members)))

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.parents == other.parents and self.members == other.members)

    def __hash__(self):
        return self._hash

    def is_namedonly_type(self):
        return True

    def map_over(self, map_func):
        # TODO(Mason): Parents

        new_members = []
        for member in self.members:
            new_subs = map_func(member)
            for new_sub_node in new_subs:
                new_members.append(new_sub_node.map_over(map_func))
        return self.__class__(parents=self.parents, members=new_members)        

    def validate(self, context):
        for p in self.parents:
            if not TypeClass.type_validate(p, context):
                return False

        for m in self.members:
            if not (isinstance(m, RootNode) and m.validate()):
                return False

        return True

    def expand_root_class(self, declare, sub_name=""):
        def map_func_named_class_replace(node, name=""):
            ret = node
            if isinstance(node, base_types.NamedType):
                if node.symbol in self._type_dict:
                     ret = base_types.NamedType(extension_prefix + node.symbol)
            if name == "":
                return [ret]
            return [(name, ret)]

        roots = []
        variable_struct_elements = {}
        for member in self.members:
            mo_member = member.map_over(map_func_named_class_replace)
            if (isinstance(mo_member, nodes.TypeDeclaration)):
                if isinstance(mo_member.type, TypeClass):
                    roots.extend(mo_member.type.expand_root_class(mo_member, declare.name))
                else:
                    roots.append(nodes.TypeDeclaration(extension_prefix + mo_member.name, mo_member.type))
            elif (isinstance(mo_member, nodes.VariableDefinition)):
                variable_struct_elements[mo_member.name] = mo_member.type
            else:
                # TODO(Mason): Custom exception:
                raise ValueError("RootNode type unknown {}".format(mo_member))

        struct_name = extension_prefix + "CLASS_" + declare.name
        roots.append(nodes.TypeDeclaration(struct_name, base_types.TypeStruct(variable_struct_elements)))

        roots.append(nodes.TypeDeclaration(declare.name, base_types.NamedType(struct_name).Pointer()))
        return roots

def expand(ast):
    new_ast = []
    for node in ast:
        if isinstance(node, nodes.TypeDeclaration) and isinstance(node.type, TypeClass):
            new_ast.extend(node.type.expand_root_class(node, ""))
        else:
            new_ast.append(node)
    return new_ast

