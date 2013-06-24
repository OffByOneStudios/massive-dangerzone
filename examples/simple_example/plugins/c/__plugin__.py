from madz.stub import *

plugin = Plugin(
    name="c",
    version="1.0.0",

    language="c",

    imports=["a", "b"],

    variables={
        "origin_distance": TypeFunction(
            TypeFloat32,
            {"x": TypeFloat32,
             "y": TypeFloat32})
    })
