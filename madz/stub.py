"""stub.py
@OffbyOneStudios 2013
A depreciated import for python plugin stubs.

Currently just forwards plugin_stub.py
"""

import logging as _logging

from .plugin_stub import *

_logger = _logging.getLogger(__name__)

_logger.warning("'from madz.stub import *' is depreciated, use 'from madz.plugin_stub import *' instead.")
