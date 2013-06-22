from madz.stub import *

plugin = Plugin(
    name="b",
    version="1.0.0",

    language="python",

    depends=["a"],

    variables={
        "origin_distance": TypeFunction(
            TypeFloat32,
            {"a": "a.Point2d"})
    })
