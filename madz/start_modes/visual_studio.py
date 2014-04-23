
from ..daemon import client

def start(argv, system, user_config):
    res = client.invoke_minion("visual_studio", (argv, user_config))

    if isinstance(res, str):
        print(res)
    else:
        for tup in res:
            print(tup)