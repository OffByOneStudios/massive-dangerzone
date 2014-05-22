from madz.plugin_stub import *

plugin = Plugin(
    namespace="target",
    executable=True,
    language="python",
    imports=[
        "driver",
        "task.c",
        "task.cpp",
        "task.python",
    ],
    
    description="var main() -> void;"
)

