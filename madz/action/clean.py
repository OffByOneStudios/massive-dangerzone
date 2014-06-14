"""action/clean.py
@OffbyOne Studios 2013
Action to clean temporary files in plugins.
"""
import logging

from ..config import *
from ..module import *
from .base import *

logger = logging.getLogger(__name__)

class CleanAction(BaseAction):
    """Manages the cleaning of temporary, and other, files from plugins."""
    action_name = "clean"

    def __init__(self, system):
        self.system = system

    def _get_provider(self, language):
        return language.make_cleaner()


