"""madzmodule:module/new/language/core/__init__.py
@OffbyOne Studios 2014
Package for generating new language files.
"""

import os

from .INewLanguage import *
from .bootstrap import *

def get_newlanguage(name):
    if name in NewLanguage_identity.current:
        return NewLanguage_identity.current[name][NewLanguage]

    else: # Try loading it
        plugin = madz.bootstrap.bootstrap_ensure_module("madzmodule.language.{}".format(name))
        try:
            return NewLanguage_identity.current[name][NewLanguage]
        except:
            pass
        return plugin[madz.bootstrap.Object]
