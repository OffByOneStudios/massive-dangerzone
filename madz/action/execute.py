"""action/execute.py
@OffbyOne Studios 2013
Action for executing a plugin.
"""
import logging

from ..config import system as system_config

logger = logging.getLogger(__name__)

class ExecuteAction(object):
    """Executes a function from a plugin."""
    def __init__(self, system):
        self.system = system

    def do(self):
        """Executes a plugin."""
        pass

