import sys, os

from ..daemon import client

def start(argv, system, user_config):
    # TODO: Replace
    res = client.invoke_daemon("banish")

    print(res)

    if not (len(argv) > 2 and argv[1] == "-r"):
        return
    print()

    print("TODO: Some restart code")
