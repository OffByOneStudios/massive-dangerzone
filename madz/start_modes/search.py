
from ..daemon import client

def start(argv, system, user_config):
    res = client.invoke_minion("search", (argv, user_config))
    for tup in res:
        print(tup)