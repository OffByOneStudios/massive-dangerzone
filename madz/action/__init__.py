"""actions/__init__.py
@OffbyOneStudios 2013
Forwards and indexs all the actions.
"""

from .build import BuildAction
from .clean import CleanAction
from .load import LoadAction
from .wrap import WrapAction
from .execute import ExecuteAction

actions = {
    "build": BuildAction,
    "clean": CleanAction,
    "load": LoadAction,
    "wrap": WrapAction,
    "execute": ExecuteAction
}
