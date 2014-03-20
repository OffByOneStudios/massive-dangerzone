from abc import *
import hashlib
import os
import os.path as path


class MadzObjectAsDirectory(metaclass=ABCMeta):
    """Interface for objects which wish to make use of a folder inside the .madz hidden directory"""
    
    @classmethod
    @abstractmethod
    def madz_folder_name(self):
        """Return the directory name required by the implementing class
        
        This name should be either a folder or a relative folder path from the .madz folder.
        """
        pass

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

        self._path = abs_path

    def open(self, file_mode="r"):
        """Open this file.

        returns:
            Python builtin file stream.
        """
        return open(abs_path, file_mode)

    def __str__(self):
        return "{} Mode File object".format(self._mode)

    def __repr__(self):
        return "File(\"{}\",\"{}\")".format(self._path, self._mode)


class Directory(object):
    """Class representing a folder of which madz is aware."""

    def __init__(self, absolute_path):
        """Constructor

        args:
            absolute_path : string directory path
        """

        self._directory = absolute_path
        self._files = [ f for f in os.listdir(absolute_path) if path.isfile(path.join(absolute_path,f))]
        if path.exists(absolute_path) == False:
            os.makedirs(absolute_path)

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
        return File(path.join(self._directory, file_name)) if file_name in self._files else None

        
class ModuleContentsDirectory(ContentsDirectory):
    """Class Representing the top level folder of a madz module"""

    def __init__(self, absolute_path):
        """Constructor

        args:
            absolute_path : string directory path
        """
        ContentsDirectory.__init__(self, absolute_path)
        self._madz = ContentsDirectory(path.join(absolute_path, ".madz"))

    @property
    def madz(self):
        """Retrieve the MADZ hidden directory"""
        return self._madz

    def madz_directory_for_type(self, the_type):
        """Get (or create) a madz subdirectory for type.
        
        Args:
            Object Type which implements the MadzObjectAsDirectory interface.
        """
        return ContentsDirectory(path.join(
                path.join(self._directory, ".madz"),
                the_type.madz_folder_name))
