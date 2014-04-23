from . import daemon, command, terminal, kill, execute, search, visual_studio

start_modes = {
    "daemon": daemon.start,
    "command": command.start,
    "terminal": terminal.start,
    "execute": execute.start,
    "kill": kill.start,
    "search": search.start,
    "visual_studio" : visual_studio.start,
}

try:
    from . import ipython
    start_modes["ipython"] = ipython.start
except:
    pass
