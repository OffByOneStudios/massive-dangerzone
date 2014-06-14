"""madz/start_mode/command.py
@OffbyOne Studios 2014
Srtartmode for executing a build command across the plugin system.
"""

from ..daemon import client

def start(argv, system, user_config):
    res = client.invoke_minion("command", (argv, user_config))

    print(res)
