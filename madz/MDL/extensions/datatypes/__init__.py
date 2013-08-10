import logging

from ... import nodes
from ... import base_types

extension_symbol = "MADZ_EXT_DATATYPES"

logger = logging.getLogger(__name__)

class TypeDatatype(base_types.TypeTypeComplex):
    """Represents a datatype, a type ment to be treated as a fundamental type.

    Currently has the following features:
        * Namespaced functions.

    Will eventually have:
        * Private data
        * Const gaurntees
        * Static compilation
        * Functional gaurntees
        * Constructor/Destructor hinting
        * Opperator overload hinting
        * Pass by value semantics
        * Type genericism

    Differences from structs:
        * Language integration
        * Functions tied to struct

    """
    def __init__(self, struct, functions=[]):
        """Takes a struct describing the data provided by the data type and some function definitions."""
        self.struct = struct
        self.functions = tuple(sorted(functions, key=lambda n: (hash(n.__class__), n.name)))
        self._hash = hash((hash(self.functions),
                          hash(struct)))

        self._func_dict = dict()
        for func in self.functions:
            self._func_dict[func.name] = func.type

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.struct == other.struct and self.functions == other.functions)

    def __hash__(self):
        return self._hash

    # Make sure we cannot be inlined
    def is_namedonly_type(self):
        return True

    def map_over(self, map_func):
        new_functions = []
        for func in self.functions:
            new_subs = map_func(func)
            for new_sub_node in new_subs:
                new_functions.append(new_sub_node.map_over(map_func))
        return self.__class__(struct=self._map_over_single_val(self, map_func, self.struct),
            functions=new_functions)

    def validate(self, context):
        if base_types.TypeStruct.type_validate(self.struct, context):
                return False

        for f in self.functions:
            if not (isinstance(m, nodes.VariableDefinition) and f.validate()):
                return False

        return True

    def expand_declare(self, declare):
        """Expands a datatype to variabledefinitions and typedeclarations using base_types."""
        if declare.type != self:
            raise ValueError("Datatype can only expand {} nodes containing itself.".format(declare.__class__))

        roots = [nodes.TypeDeclaration(declare.name, self.struct)]

        for function in self.functions:
            if (isinstance(function, nodes.VariableDefinition)):
                function_name = "{extension_symbol}_{dt_name}_FUNCTION_{func_name}".format(
                    extension_symbol=extension_symbol,
                    dt_name=declare.name,
                    func_name=function.name)
                roots.append(nodes.VariableDefinition(name = function_name, type = function.type))
            else:
                # TODO(Mason): Custom exception:
                raise ValueError("RootNode type unknown {}".format(mo_member))
        return roots

def expand(ast):
    new_ast = []
    for node in ast:
        if isinstance(node, nodes.TypeDeclaration) and isinstance(node.type, TypeClass):
            new_ast.extend(node.type.expand_declare(node))
        else:
            new_ast.append(node)
    return new_ast

