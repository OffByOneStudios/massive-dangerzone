import os, sys

def get_system_description():
    """Returns a string representation of the current operating system name."""
    if sys.platform =="darwin":
        return "osx"
    elif os.name == "nt":
        return "windows"
    elif os.name == "posix" or os.name == "mac":
        return "unix"

_systems = {}

def get_system():
    """Returns the system description of the current operating system."""
    sysd = get_system_description()

    if not (sysd in _systems):
        if sysd == "windows":
            from . import windows
            _systems["windows"] = windows.WindowsOperatingSystem()

        elif sysd == "unix":
            from . import unix
            _systems["unix"] = unix.UnixOperatingSystem()

        elif sysd == "osx":
            from . import unix
            _systems["osx"] = unix.UnixOperatingSystem()
        else:
            raise NotImplementedError(os.name)

    return _systems[sysd]