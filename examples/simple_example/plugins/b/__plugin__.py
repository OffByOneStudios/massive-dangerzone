from madz.stub import *

plugin = Plugin(
    name="b",
    version="1.0.0",

    language="c",

    depends=["a"],

    description={
        VariableDefinition("origin", "a.Point2d"),
        VariableDefinition("origin_distance",
            TypeFunction(
                TypeFloat32,
                [TypeFunctionArgument("a", "a.Point2d")]))
    })
