"""madz/start_mode/command.py
@OffbyOne Studios 2014
Srtartmode for executing a build command across the plugin system.
"""

from ..daemon import Client

def start(argv, system, user_config):
    res = Client().invoke_minion("command", (argv, user_config))

    print(res)
