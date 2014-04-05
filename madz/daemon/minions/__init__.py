

from .command import CommandMinion
from .executer import ExecuterMinion
from .search import SearchMinion

raw_handlers={
    "command": CommandMinion,
    "search": SearchMinion,
    "execute": ExecuterMinion
}

try:
    from .ipython import InteractivePythonMinion
    raw_handlers["ipython"] = InteractivePythonMinion
except:
    pass
