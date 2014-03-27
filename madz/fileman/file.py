import os
import os.path as path

import re

from .core import *

class File(IPathable):
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
    def path(self):
        return self._path

    @property
    def basename(self):
        """Return String base filename (no path)"""
        return path.basename(self._path)

    def exists(self):
        """Returns True if the file pointed to by this path exists False otherwise"""
        return FileManager.current.exists(self)

    def modify(self):
        FileManager.current.modify(self)

    def open(self, file_mode="r"):
        """Open this file.

        returns:
            Python builtin file stream.
        """
        FileManager.current.ensureDirectory(self)

        return FileManager.current.openFile_Python(self, file_mode)

    def with_directory(self, directory):
        if not isinstance(directory, IPathable):
            raise Exception("Can only rebase file to pathable directory, not {}.".format(directory))
        path, fname = os.path.split(self._path)

        return File(os.path.join(directory.path, fname))

    def with_extension(self, extension):
        """Construct a new copy of this file with its extension changed"""
        path, fname = os.path.split(self._path)

        fname = ".".join(fname.split(".")[:-1] + [extension])
        return File(os.path.join(path, fname))

    @property
    def modify_date(self):
        if not (self.exists()):
            return None
        return path.getmtime(self._path)

    def __str__(self):
        return "{}".format(self._path)

    def __repr__(self):
        return "File(\"{}\")".format(self._path)

    def _key(self):
        return (self._path,)

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        return isinstance(other, File) and self._key() == other._key()