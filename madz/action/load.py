"""action/load.py
@OffbyOneStudios 2013
Action to load plugins.
"""
import logging

from .. import operating_system

from .base import *

import os

logger = logging.getLogger(__name__)

class LoadAction(BaseAction):
    """Loads plugins into the program's memory space and provides access to them."""
    action_name = "load"

    forked = False

    def __init__(self, system):
        BaseAction.__init__(self, system)
        self._operating = operating_system.get_system()

    class LoadProvider(object):
        """Temporary placeholder for future load providers."""
        def __init__(self, plugin_stub, operating_system):
            self.plugin_stub = plugin_stub
            self.operating_system = operating_system

        def get_dependency(self):
            return False

        def do(self):
            self.operating_system.load(self.plugin_stub)

    def _get_provider(self, language):
        return self.LoadProvider(language.plugin_stub, self._operating)

    def do(self, *args, **kwargs):
        if not (self.forked):
            print("!!!! -- PREFORK -- !!!!")
            LoadAction.forked = True
            ret = os.fork()
            if (ret != 0):
                os.waitpid(ret, 0)
                exit()
        return super().do(*args, **kwargs)
