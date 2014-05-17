
from .command import CommandMinion
from .executer import ExecuterMinion
from .search import SearchMinion
from .visual_studio import VisualStudioMinion

try:
    from .ipython import InteractivePythonMinion
except:
    pass
