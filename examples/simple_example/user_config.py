from madz.user_config import *

# This is an example of a user config file. These are used to provide
# machine specific information to madz.

# Choose operating system
user_os_choice = { "windows" : 0, "linux" : 1, "macosx" : 2}["windows"]
# Prefered compiler. Options cl, mingw, gcc, clang
user_compiler_preference = "mingw"

# The Python3 installation used to run madz
user_runtime_python = ["C:\\Python33", "/usr/bin/python34", "/usr/local/Cellar/python3/3.4.1/Frameworks/Python.framework/Versions/3.4/"][user_os_choice]

config = UserConfig([
    # Choose a C compiler, "gcc" and "clang" for unix.
    # "cl" or "mingw" for windows. The compiler must be accessible on the path.
    # For windows/cl this means running vcvarsall before starting the daemon.
    OptionCompilerPreference(user_compiler_preference),
    OptionCompilerDebug(1.0),

    LanguageConfig("python", [
        # Path locations only required for windows
        OptionHeaderSearchPaths([
            os.path.join(user_runtime_python, "include", *(["python3.4m"] if user_os_choice == 2 else [])),
        ]),
        OptionLibrarySearchPaths([
            os.path.join(user_runtime_python, ["libs", "", "lib"][user_os_choice]),
        ]),
        OptionLibraryStaticLinks([["python3", "python3", "python3.4"][user_os_choice]]),
        #OptionLibraryFrameworks(["Python"]),
    ]),
])
