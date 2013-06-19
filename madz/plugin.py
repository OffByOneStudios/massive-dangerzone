import os, sys
import imp

class PluginIndex(object):
    """A value type for uniquely identifying plugins."""
    def __init__(self, namespace, version, implementation_name):
        self.namespace = namespace
        self.version = version
        self.implementation_name = implementation_name

    @classmethod
    def parse(cls, relative):
        """Parses a canoical string into a PluginIndex"""
        # TODO(Mason): Exception types
        relativestring = relative

        version_string = None
        version_start = relativestring.find('[')
        version_end = relativestring.find(']')
        if (version_start == -1) ^ (version_start == -1):
            raise Exception
        elif version_start != -1:
            version_string = relativestring[version_start+1:version_end]
            relativestring = relativestring[:version_start] + relativestring[version_end+1:]
            
        implname_string = None
        implname_start = relativestring.find('[')
        implname_end = relativestring.find(']')
        if (implname_start == -1) ^ (implname_start == -1):
            raise Exception
        elif version_start != -1:
            implname_string = relativestring[implname_start+1:implname_end]
            relativestring = relativestring[:implname_start] + relativestring[implname_end+1:]

        return cls(relativestring, version_string, implname_string)

    def as_tuple(self):
        """Returns a tuple for uniquely indentifying the PluginIndex"""
        return (self.namespace, self.version, self.implementation_name)

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __repr__(self):
        return "PluginIndex{!r}".format(self.as_tuple())

class PythonPluginDescription(object):
    """An object representing a python plugin description.

    Python plugin descriptions are represented as a '__plugin__.py' file in the plugin directory.

    """
    def __init__(self, directory):
        """Attempts to load a python description from the directory given."""
        # TODO(Mason): Exception for plugin file not found
        self._py_module_filename = os.path.join(directory, "__plugin__.py")

        self._init_module()

    @classmethod
    def contains_description(cls, directory):
        """Returns true if the directory contains a potential python plugin description."""
        return os.path.exists(os.path.join(directory, "__plugin__.py"))

    def _init_module(self):
        with open(self._py_module_filename) as module_file:
            # TODO(Mason): Exception for failure to load
            # TODO(Mason): Figure out name variable
            self.module = imp.load_module("test", module_file, self._py_module_filename, ('.py', 'r', imp.PY_SOURCE))

    def _get(self, name):
        """Gets an arbitrary value from the loaded plugin file."""
        return (getattr(self.module, name) if hasattr(self.module, name) else None)

    def get_index_tuple(self):
        """Returns the PluginIndex described by the description file."""
        return (self._get("namespace"), self._get("version"), self._get("implementation_name"))

class PluginStub(object):
    """A helper container for the index, description, and directory of a plugin."""
    def __init__(self, index, description, directory):
        self.index = index
        self.description = description
        self.directory = directory

class PluginDirectory(object):
    def __init__(self, system, directory, sub_namespace):
        self.system = system
        self.directory = directory
        self.sub_namespace = sub_namespace

        self._stubs = {}

        self._init_plugins()

    def _add_stub(self, stub):
        self._stubs[stub.index] = stub
        self.system._add_plugin_stub(stub)

    def _init_plugins(self):
        for root, dirs, files in os.walk(self.directory):
            relroot = os.path.relpath(root, self.directory)
            splitrelroot = relroot.split(os.sep)

            for d in splitrelroot:
                if d.startswith('.'):
                    continue

            if PythonPluginDescription.contains_description(root):
                description = PythonPluginDescription(root)
                file_pieces = PluginIndex.parse(".".join(splitrelroot)).as_tuple()
                desc_pieces = description.get_index_tuple()
                match = \
                    reduce(lambda a, i: a and i,
                        map(lambda a, b: a == b or ((a is None) != (b is None)),
                            file_pieces, desc_pieces))
                if not match:
                    raise Exception # TODO(Mason): better exception
                merged = map(lambda a, b: a or b, file_pieces, desc_pieces)
                index = PluginIndex(*merged)

                self._add_stub(PluginStub(index, description, root))

class PluginSystem(object):
    """ A plugin system object which manages a root namespace of objects.

    Responsible for compiling togeather and then loading plugins across language boundries.

    """
    def __init__(self, rootname):
        self.rootname = rootname
        self.directories = []
        self.plugin_stubs = {}

    @staticmethod
    def _join_namespaces(first, second):
        splitfirst = first.split('.')
        splitsecond = second.split('.')

        return ".".join(splitfirst + splitsecond)

    def _add_plugin_stub(self, plugin_stub):
        self.plugin_stubs[plugin_stub.index] = plugin_stub

    def load_plugin_directory(self, directory, sub_namespace=""):
        self.directories.append(PluginDirectory(self, directory, sub_namespace))

