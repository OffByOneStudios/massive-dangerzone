"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys, shutil
import logging
import subprocess

from madz.languages.c import clean as cclean
from madz.dependency import Dependency

logger = logging.getLogger(__name__)

class Cleaner(cclean.Cleaner):
    pass