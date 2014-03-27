# Add null logging handler
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.getLogger(__name__).setLevel(logging.DEBUG)

# Add htn
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "htn"))
