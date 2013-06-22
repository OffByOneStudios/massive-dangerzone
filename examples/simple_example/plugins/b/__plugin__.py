from madz.stub import *

plugin = Plugin(
    name="b",
    version="1.0.0",

    language="c",

    depends=["a"],

    variables={
        "origin" : "Point2d",
        "origin_distance": TypeFunction(
            TypeFloat32,
            {"a": "a.Point2d"})
    })
