"""action/wrap.py
@OffbyOne Studios 2013
Action for building wrapper files.
"""
import logging

from ..config import *
from .base import *

logger = logging.getLogger(__name__)

class WrapAction(BaseAction):
    """Generates inter-language wrapper files required by a plugin."""
    action_name = "wrap"

    def __init__(self, system):
        self.system = system

    def _get_provider(self, language):
        return language.make_wrapper()

