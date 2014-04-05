from . import daemon, command, terminal, kill, search

start_modes = {
    "daemon": daemon.start,
    "command": command.start,
    "terminal": terminal.start,
    "kill": kill.start,
    "search": search.start
}

try:
    from . import ipython
    start_modes["ipython"] = ipython.start
except:
    pass
