from madz.plugin_stub import *

plugin = Plugin(
    namespace="task.c",
    
    language="c",
    depends=[
        "task"
    ],
    
    description=MdlFileLoader("task.mdl"),
)

