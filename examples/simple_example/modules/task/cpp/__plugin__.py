from madz.plugin_stub import *

plugin = Plugin(
    namespace="task.cpp",
    
    language="cpp",
    depends=[
        "task"
    ],
    imports=[
        "driver"
    ],
    
    description=MdlFileLoader("task.mdl"),
)

