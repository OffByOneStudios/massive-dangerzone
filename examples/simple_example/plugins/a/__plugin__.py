from madz.stub import *

plugin = Plugin(
    name="a",
    version="1.0.0",

    language="c",

    declarations={
        "Point2d": TypeStruct({
            "x": TypeFloat32,
            "y": TypeFloat32,
        })
    },
    variables={
        "a_var" : TypeInt32,
        "origin" : "Point2d",
        "distance": TypeFunction(
            TypeFloat32,
            {"a": "Point2d",
             "b": "Point2d"})
    }
)
