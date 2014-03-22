from ctypes import *
from abc import *
import hashlib
import logging
import os
import os.path as path

from .file import File

logger = logging.getLogger(__name__)

def contents_directory(obj):

    if isinstance(obj, Directory) or isinstance(obj, ModuleContentsDirectory):
        return ContentsDirectory(obj._directory)

    raise TypeError("Cannot convert from type :{} to type ContentsDirectory".format(type(obj)))


class Directory(object):
    """Class representing a folder of which madz is aware."""

    def __init__(self, absolute_path):
        """Constructor

        args:
            absolute_path : string directory path
        """
        
        # Ensure path is absolute
        self._directory = path.abspath(absolute_path)

        if path.exists(absolute_path) == False:
            os.makedirs(absolute_path)

        self._files = [ f for f in os.listdir(absolute_path) if path.isfile(path.join(absolute_path,f))]
     
    @staticmethod
    def _fullname(o):
        """Fully qualified typename of object o
        
            Ref: http://stackoverflow.com/questions/2020014/get-fully-qualified-class-name-of-an-object-in-python
        """
        return o.__module__ + "." + o.__name__
    
    def subdirectory(self, *args):
        return Directory(path.join(self._directory, *args))

    def subdirectory_for_type(self, the_type):
        return Directory(path.join(self._directory, self._fullname(the_type)))

    def files(self, extension_filter=[]):
        """Get Files in this directory

        args:
            extension_filter : List of file extensions without '.'
        """
        return [File(path.join(self._directory, f)) for f in self._files if len(extension_filter) == 0 or f.split(".")[1] in extension_filter]

    def file_names(self, extension_filter=[]):
        """Get Files in this directory

        args:
            extension_filter : List of file extensions without '.'
        """
        return [f for f in self._files if len(extension_filter) == 0 or f.split(".")[1] in extension_filter]

    def file_hashes(self):
        """Calculate hashes of files. Used to test file changes. 
        
        Returns:
            Dictionary of file path, hash pairs.
        """

        res = dict()

        for f in self._files:
            m = hashlib.sha256()
            with open(path.join(self._directory, f)) as o:
                m.update(o.read().encode('utf-8'))

            res[f] = m.hexdigest()

        return res

    def files_modified(self):
        """Calculate date modified of files. Used to test file changes. 
        
        Returns:
            Dictionary of file path, date modified pairs.
        """
        res = dict()

        for f in self._files:
            res[f] = path.getmtime(path.join(self._directory, f))

        return res

    def hashes_changed(self, hash_table):
        """ Returns a list of file objects whose hashes differ from the provided hash table.

        This hash table would have been generated using file_hashes.
        
        Args:
            hash_table : dictionary of filename hash pairs.
        """
        res = []
        current_hashes = self.file_hashes()
        for key, value in hash_table.items():
            if current_hashes.get(key) != value:
                res.append(File(path.join(self._directory, key)))
            
        return res if len(res) > 0 else None

    def datetimes_changed(self, target_file):
        """ Returns a list of file objects whose datetimes differ from the provided datetime table.

        This hashdatetime_table would have been generated using files_modified.
        
        args:
            target_file : Relative path to target file.

        Returns:
            List of files whose modified dates are greater than 
        """
        time = path.getmtime(path.join(self._directory, f))

        res = []
        current_times = self.files_modified()
        for key, value in current_times.items():
            if value > time:
                res.append(File(path.join(self._directory, key)))
            
        return res if len(res) > 0 else None

    def as_string(self):
        """Returns the absolute path to directory referenced by this object."""
        return self._directory

    def __str__(self):
        return self._directory

class ContentsDirectory(Directory):
    """Class representing the directory contents of a Madz plugin."""

    def __init__(self, absolute_path):
        """Constructor

        args:
            absolute_path : string directory path
        """
        Directory.__init__(self, absolute_path)

    def file(self, file_name):
        """Retrieve file

        args:
            file_name : "String relative path of file"
        """
        return File(path.join(self._directory, file_name))

    def file_exists(self, file_name):
        """Returns True if file_name exists, false otherwise"""
        return  path.exists(path.join(self._directory, file_name))

    @classmethod
    def from_Directory(cls, the_directory):
        """Coerce a directory into a contents directory
        
        By default calls to subdirectory constructs Directory objects, which prohibit individual file access.
        For code which needs to access a specific file, one should use this class method to build a contents directory

        """ 
        return ContentsDirectory(the_directory._directory)

class ModuleContentsDirectory(ContentsDirectory):
    """Class Representing the top level folder of a madz module
    
    Members:
        madz : The ".madz" hidden folder. Madz machinery lives here. Not for prying eyes.
    """

    def __init__(self, absolute_path):
        """Constructor

        args:
            absolute_path : string directory path
        """
        ContentsDirectory.__init__(self, absolute_path)

        self._madz = ContentsDirectory(path.join(absolute_path, ".madz"))
        if os.name == "nt":
            try:
                #Hide the .madz folder on windows logger
                ret = windll.kernel32.SetFileAttributesW(str(self._madz), 0x02)
                if ret == 0:
                    logger.warn("Unable to mark .madz directory as hidden in plugin folder:{}.".format(absolute_path))
            except Exception as e:
                logger.warn("Unable to mark .madz directory as hidden in plugin folder:{}.".format(absolute_path))

    @property
    def madz(self):
        """Retrieve the MADZ hidden directory"""
        return self._madz

    def subdirectory(self, *args):
        if(args[0] == ".madz"):
            return self.madz
        else:
            return super().subdirectory(*args)
