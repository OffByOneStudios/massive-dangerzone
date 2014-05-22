from madz.plugin_stub import *

plugin = Plugin(
    namespace="task.python",
    
    language="python",
    depends=[
        "task"
    ],
    
    description=MdlFileLoader("task.mdl"),
)

