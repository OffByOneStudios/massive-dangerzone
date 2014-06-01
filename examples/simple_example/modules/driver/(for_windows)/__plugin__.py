from madz.plugin_stub import *

plugin = Plugin(
    namespace="driver",
    
    language="cpp",
    depends=[
        "task"
    ],
    imports=[
        "task.cpp"
    ],
    
    description=MdlFileLoader("driver.mdl"),
)

