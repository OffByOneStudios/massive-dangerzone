import os

def get_system_description():
    if os.name == "nt":
        return "windows"
    elif os.name == "posix" or os.name == "mac":
        return "unix"

def get_system():
    sysd = get_system_description()

    if sysd == "windows":
        from . import windows
        return windows.WindowsOperatingSystem()

    elif sysd == "unix":
        from . import unix
        return unix.UnixOperatingSystem()

    else:
        raise NotImplementedError(os.name)
