# Add null logging handler
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.getLogger(__name__).setLevel(logging.DEBUG)

# Load extensions
import os as _os

def _try_load_pydepend(depname, optional=False):
    import importlib
    import traceback
    import sys
    import os
    
    try:
        importlib.import_module(depname)
    except Exception as e:
        tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
        print("===> Python library '{}' failed to load:\n\t{}".format(depname, tb_string))

_try_load_pydepend("zmq")
        
from . import bootstrap

from .bootstrap import _extensions
_extensions.load_extensions(_os.path.join(_os.path.dirname(__file__), "..", "madz_extension"))