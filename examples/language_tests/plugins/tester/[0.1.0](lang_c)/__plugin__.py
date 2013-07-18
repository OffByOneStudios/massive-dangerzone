from madz.stub import *

plugin = Plugin(
    name="tester",

    language="c",

    imports=["c.set0"],
    active = False
    description=[
        VariableDefinition("test",
            TypeFunction(
                TypeNone,
                []))
    ])
