from madz.plugin_stub import *

plugin = Plugin(
    namespace="driver",
    
    language="cpp",
    depends=[
        "task"
    ],
    
    description=MdlFileLoader("driver.mdl"),
)

