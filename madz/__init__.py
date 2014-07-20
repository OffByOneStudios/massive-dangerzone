# Add null logging handler
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.getLogger(__name__).setLevel(logging.DEBUG)

# Load extensions
import os
from . import bootstrap

from .bootstrap import _extensions
_extensions.load_extensions(os.path.join(os.path.dirname(__file__), "..", "madz_extension"))