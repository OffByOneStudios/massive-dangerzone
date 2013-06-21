from madz.stub import *

plugin = Plugin(
    name="a",
    version="1.0.0",

    language="c",

    declarations={
        "Point2d": TypeStructType({
            "x": TypeFloat32(),
            "y": TypeFloat32(),
        }),
        "distance": TypeFunction(
            TypeFloat32(),
            {"a": TypeStructVar("Point2d"),
             "b": TypeStructVar("Point2d")})
    })
