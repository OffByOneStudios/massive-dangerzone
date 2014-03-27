from . import daemon, command, terminal

start_modes = {
    "daemon": daemon.start,
    "command": command.start,
    "terminal": terminal.start,
}

try:
    from . import ipython
    start_modes["ipython"] = ipython.start
except:
    pass
