import os
def get_system():
    if os.name =="nt":
        import windows
        return windows.WindowsOperatingSystem()

    elif os.name == "posix":
        import unix
        return unix.UnixOperatingSystem()

    elif os.name == "mac":
        import unix
        return unix.UnixOperatingSystem()

    else:
        raise NotImplementedError(os.name)
