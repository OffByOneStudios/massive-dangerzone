from madz.stub import *

plugin = Plugin(
    name="base_c.b",
    version="1.0.0",

    language="c",

    depends=["base_c.a"],

    description={
        VariableDefinition("origin", "base_c.a.Point2d"),
        VariableDefinition("origin_distance",
            TypeFunction(
                TypeFloat32,
                [TypeFunctionArgument("a", "base_c.a.Point2d")]))
    })
