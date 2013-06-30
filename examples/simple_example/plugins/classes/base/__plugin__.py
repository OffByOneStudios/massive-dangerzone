from madz.pyMDL import *

plugin = Plugin(
    version="1.0.0",

    language="c",

    description=[
        TypeDeclaration("base_class", 
            TypeClass([], [
                TypeDeclaration("my_int", TypeInt64),
                VariableDefinition("inty", TypeUInt32),
                VariableDefinition("my_int", "my_int"),
                VariableDefinition("a_func",
                    TypeFunction(
                        "my_int",
                        [TypeFunctionArgument("a", "my_int"),
                         TypeFunctionArgument("b", "my_int")]))
                ])),
        VariableDefinition("foo", "base_class")
    ])
