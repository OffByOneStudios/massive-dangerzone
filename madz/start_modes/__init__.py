from . import daemon, command, ipython, terminal

start_modes = {
    "daemon": daemon.start,
    "command": command.start,
    "ipython": ipython.start,
    "terminal": terminal.start,
}
