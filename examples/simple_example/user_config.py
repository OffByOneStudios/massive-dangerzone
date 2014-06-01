from madz.user_config import *

# This is an example of a user config file. These are used to provide
# machine specific information to madz.

# Choose operating system
user_os_choice = { "windows" : 0, "linux" : 1, "macosx" : 2}["windows"]
# Prefered compiler. Options cl, mingw, gcc, clang
user_compiler_preference = "mingw"

# The Python3 installation used to run madz
user_runtime_python = ["C:\\Python33", "/usr/bin/python34"][user_os_choice]

config = UserConfig([
    # Choose a C compiler, "gcc" and "clang" for unix.
    # "cl" or "mingw" for windows. The compiler must be accessible on the path.
    # For windows/cl this means running vcvarsall before starting the daemon.
    OptionCompilerPreference(user_compiler_preference),
    OptionCompilerDebug(1.0),
    
    LanguageConfig("python", [
        # Path locations only required for windows
        OptionHeaderSearchPaths([
            os.path.join(user_runtime_python, "include"),
        ]),
        OptionLibrarySearchPaths([
            os.path.join(user_runtime_python, "libs"),
        ]),
        OptionLibraryStaticLinks(["python33"])
    ]),
])
