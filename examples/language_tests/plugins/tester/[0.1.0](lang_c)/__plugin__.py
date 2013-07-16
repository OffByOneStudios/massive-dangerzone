from madz.stub import *

plugin = Plugin(
    name="tester",

    language="c",

    imports=["c.set0"],

    description=[
        VariableDefinition("test",
            TypeFunction(
                TypeNone,
                []))
    ])
