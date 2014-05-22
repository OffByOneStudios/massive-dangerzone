from madz.plugin_stub import *

plugin = Plugin(
    namespace="task.cpp",
    
    language="cpp",
    depends=[
        "task"
    ],
    
    description=MdlFileLoader("task.mdl"),
)

