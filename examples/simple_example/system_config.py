from madz.system_config import *

# This file describes the system. This config is meant to be independent of
# the specifc machine being run on, although it may change configuration for
# different platforms using imposters.

config = SystemConfig([
    LibraryConfig("windows", [
        OptionLibraryStaticLinks(["Kernel32", "user32", "gdi32"]),
    ]),
    
    LibraryConfig("pthread", [
        OptionLibraryStaticLinks(["pthread"])
    ]),
])
