from madz.user_config import *

# This is an example of a user config file. These are used to provide
# machine specific information to madz. 

config = UserConfig([
    # Choose a C compiler, "gcc" and "clang" for unix.
    # "cl" or "mingw" for windows. The compiler must be accessible on the path.
    # For windows this means running vcvarsall before starting the daemon.
    OptionCompilerPreference("mingw"),
    OptionCompilerDebug(1.0),
    
    # Configure the python language for this machine
    LanguageConfig("python", [
        # Path locations only required for windows
        OptionHeaderSearchPaths([
            "C:\\Python33\\include",
        ]),
        OptionLibrarySearchPaths([
            "C:\\Python33\\libs",
        ]),
        # Always need the library to link:
        OptionLibraryStaticLinks(["python33"])
    ]),
])
