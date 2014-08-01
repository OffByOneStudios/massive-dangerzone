"""madz/daemon/__init__.py
@OffbyOne Studios 2014
Daemon namespace.
"""

import pydynecs

import madz.bootstrap
from madz.daemon.minion.core import *

daemon_filename = ".madz-daemon"

from .Daemon import *
from .Client import *