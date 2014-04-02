"""actions/__init__.py
@OffbyOneStudios 2013
Forwards and indexs all the actions.
"""

from .clean import *
from .wrap import *
from .build import *
from .execute import *

actions = {
    "build": BuildAction,
    "clean": CleanAction,
    "wrap": WrapAction,
    "execute": ExecuteAction
}
