from madz.plugin_stub import *

plugin = Plugin(
    namespace="driver",
    
    platform_check=PlatformCheckWindows,
    
    language="cpp",
    depends=[
        "task"
    ],
    imports=[
        "task.cpp"
    ],
    
    description=MdlFileLoader("driver.mdl"),
)

