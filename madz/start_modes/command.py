
from ..daemon import client

def start(argv, system, user_config):
    res = client.invoke_minion("command", (argv, user_config))

    print(res)
