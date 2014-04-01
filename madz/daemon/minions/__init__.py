

from .command import CommandMinion
from .executer import ExecuterMinion

raw_handlers={
    "command": CommandMinion
}

try:
    from .ipython import InteractivePythonMinion
    raw_handlers["ipython"] = InteractivePythonMinion
except:
    pass
