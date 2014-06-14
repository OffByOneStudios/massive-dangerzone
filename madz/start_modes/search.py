"""madz/start_mode/search.py
Startmode for searching available information with in the module system.
"""

from ..daemon import client

def start(argv, system, user_config):
    res = client.invoke_minion("search", (argv, user_config))

    if isinstance(res, str):
        print(res)
    else:
        for tup in res:
            print(tup)