from madz.stub import *

plugin = Plugin(
    name="base_python.d",
    version="1.0.0",

    language="python",

    imports=["base_python.c"],

    description=[
        TypeDeclaration("Point3d",
            TypeStruct({
                "x" : TypeFloat32,
                "y" : TypeFloat32,
                "z" : TypeFloat32,
                "foo" :TypePointer(TypeFloat32)
            }), doc="A Point in 3R"),
        VariableDefinition("a_var", TypeInt32),
        VariableDefinition("a_uvar", TypeUInt32),
        VariableDefinition("origin", "Point3d"),
        VariableDefinition("distance",
            TypeFunction(
                TypeFloat32,
                [TypeFunctionArgument("a", "Point3d"),
                 TypeFunctionArgument("b", "Point3d")]))
    ]
)
