

from .command import CommandMinion
from .executer import ExecuterMinion
from .search import SearchMinion
from .visual_studio import VisualStudioMinion
raw_handlers={
    "command": CommandMinion,
    "search": SearchMinion,
    "execute": ExecuterMinion,
    "visual_studio" : VisualStudioMinion,
}

try:
    from .ipython import InteractivePythonMinion
    raw_handlers["ipython"] = InteractivePythonMinion
except:
    pass
