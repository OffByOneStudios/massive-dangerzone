"""language.py
@OffbyoneStudios 2013
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob
import re

from .madz.languages.c import language as clanguage
from . import clean
from . import load
from . import build, compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguageStatic(clanguage.LanguageC):
    pass