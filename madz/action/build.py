"""action/build.py
@OffbyOne Studios 2013
Action for building plugin source code into binaries.
"""
import logging

from ..config import *
from .base import *

logger = logging.getLogger(__name__)

class BuildAction(BaseAction):
    """Builds plugin source code into binaries."""
    action_name = "build"

    def __init__(self, system):
        self.system = system

    def _get_provider(self, language):
        return language.make_builder()

