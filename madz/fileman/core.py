
import abc
import os
import os.path as path
import hashlib
from datetime import datetime

class IPathable(object):
    @property
    @abc.abstractmethod
    def path(self):
        """The path of the file object this is representing."""
        pass

class FileManager(object):
    """Represents the state of all current files.

    This is replaced by a fake object during planning."""
    current = None

    def __init__(self):
        self._directories = {}

        self._hashes = {}
        self._modified = {}
        self._times = {}

    @staticmethod
    def _to_path(path):
        if isinstance(path, str):
            return path
        if isinstance(path, IPathable):
            return path.path
        raise Exception("Can't canonicalize path.")

    def _add_file_to_directories(self, path):
        (base, file) = os.path.split(path)
        if not file: # is directory
            return
        self._directories[base] = file

    def _cache_file(self, path):
        time = path.getmtime(path)
        if (path in self._times 
            and self._times[path] == time
            and path in self._hashes):
            # We've already cached this file's hash, no need to do that again
            return

        self._times[path] = time

        m = hashlib.sha256()
        with open(path, "r") as o:
            m.update(o.read().encode('utf-8'))
        self._hashes[path] = m.digest()

    def modify(self, path):
        path = FileManager._to_path(path)

        self._add_file_to_directories(path)
        self._modified[path] = datetime.now()

    def exists(self, path):
        path = FileManager._to_path(path)

        res = os.path.exists(path)
        if res: self._add_file_to_directories(path)
        return res

    def ensureDirectory(self, path):
        path = FileManager._to_path(path)

        dir_path = os.path.dirname(path)
        if not self.exists(dir_path):
            os.makedirs(dir_path)

    def filesInDirectory(self, path):
        path = FileManager._to_path(path)

        if not (self.exists(path)):
            return []
        return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    def openFile_Python(self, path, file_mode):
        path = FileManager._to_path(path)

        self._add_file_to_directories(path)
        if not (file_mode.startswith("r")):
            self.modify(path)

        return open(path, file_mode)

if (FileManager.current is None):
    FileManager.current = FileManager()
