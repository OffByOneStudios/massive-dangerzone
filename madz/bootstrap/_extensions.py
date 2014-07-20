"""bootstrap/_extensions.py
@OffbyOneStudios 2013
Loads extensions to the bootsrapped module system.
"""

import sys
import os
import importlib
import importlib.abc

def load_extensions(extension_dir):
    sys.path.append(extension_dir)
    extlist = []
    for dir in os.listdir(extension_dir):
        fulldir = os.path.join(extension_dir, dir, "madz")
        if os.path.isdir(fulldir):
            sys.modules["madz"].__path__.append(fulldir)
            extlist += [dir]
    
    print ("Extensions:", extlist)
    