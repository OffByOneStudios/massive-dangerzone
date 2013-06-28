from madz.stub import *

plugin = Plugin(
    name="a",
    version="1.0.0",

    language="c",

    description=[
        TypeDeclaration("Point2d", 
            TypeStruct({
                "x": TypeFloat32,
                "y": TypeFloat32,
            })),
        VariableDefinition("a_var", TypeInt32),
        VariableDefinition("origin", "Point2d"),
        VariableDefinition("distance", 
            TypeFunction(
                TypeFloat32,
                [TypeFunctionArgument("a", "Point2d"),
                 TypeFunctionArgument("b", "Point2d")]))
    ]
)
