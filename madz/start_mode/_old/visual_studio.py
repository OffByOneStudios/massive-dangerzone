"""madz/start_mode/visual_studio.py
@OffbyOne Studios 2014
Startmode for integrating with visual studio.
"""

from ..daemon import Client

def start(argv, system, user_config):
    res = Client().invoke_minion("visual_studio", (argv, user_config))

    if isinstance(res, str):
        print(res)
    else:
        for tup in res:
            print(tup)