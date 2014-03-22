import os
import os.path as path

import re

class File(object):
    """Wrapper class representing a file of which madz is aware.
    
    This class wraps builtin file for the purpose of representing a file whose stream is not yet  open.
    """

    def __init__(self, abs_path):
        """Constructor

        args: 
            abs_path : absolute path to file.
            file_mode : mode to open file in.
        """
        # Ensure path is absolute
        
        self._path = path.abspath(abs_path)
    
    @property
    def basename(self):
        """Return String base filename (no path)"""
        return path.basename(self._path)

    def exists(self):
        """Returns True if the file pointed to by this path exists False otherwise"""
        return os.path.exists(self._path) 

    def open(self, file_mode="r"):
        """Open this file.

        returns:
            Python builtin file stream.
        """
        return open(self._path, file_mode)

    def with_extension(self, extension):
        """Construct a new copy of this file with its extension changed"""
        path, fname = os.path.split(self._path)

        fname = ".".join(fname.split(".")[:-1] + [extension])
        return File(os.path.join(path, fname))

    @property
    def modify_date(self):
        return path.getmtime(self._path)     

    def __str__(self):
        return "{}".format(self._path)

    def __repr__(self):
        return "File(\"{}\")".format(self._path)