from madz.stub import *

plugin = Plugin(
    name="b",
    version="1.0.0",

    language="python",

    dependencies=["a"],

    declarations={
        "origin_distance": TypeFunction(
            TypeFloat32(),
            {"a": "a.Point2d"})
    })
