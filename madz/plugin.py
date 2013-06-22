import os, sys
import imp
import pyMDL.plugin
class PluginError(Exception): pass

class PluginId(object):
    """A value type for uniquely identifying plugins."""
    def __init__(self, namespace, version, implementation_name="default"):
        self.namespace = namespace
        self.version = version
        self.implementation_name = implementation_name

    class NotAPluginIdString(PluginError): pass

    @classmethod
    def parse(cls, relative):
        """Parses a canoical plugin id string into a PluginIndex"""
        relativestring = relative

        version_string = None
        version_start = relativestring.find('[')
        version_end = relativestring.find(']')
        if (version_start == -1) ^ (version_start == -1):
            raise NotAPluginIdString("Cannot contain ']' or '[' except as version delimiters.")
        elif version_start != -1:
            version_string = relativestring[version_start+1:version_end]
            relativestring = relativestring[:version_start] + relativestring[version_end+1:]

        implname_string = None
        implname_start = relativestring.find('(')
        implname_end = relativestring.find(')')
        if (implname_start == -1) ^ (implname_start == -1):
            raise NotAPluginIdString("Cannot contain ')' or '(' except as version delimiters.")
        elif version_start != -1:
            implname_string = relativestring[implname_start+1:implname_end]
            relativestring = relativestring[:implname_start] + relativestring[implname_end+1:]

        return cls(relativestring, version_string, implname_string)

    def as_tuple(self):
        """Returns a tuple for uniquely indentifying the PluginIndex"""
        return (self.namespace, self.version, self.implementation_name)

    def __hash__(self):
        return hash(self.as_tuple())

    def compatible(self, other):
        return \
            reduce(lambda a, i: a and i,
                map(lambda a, b: a == b or ((a is None) != (b is None)),
                    self.as_tuple(), other.as_tuple()))

    def merge(self, other):
        return PluginId(*map(lambda a, b: a or b, self.as_tuple(), other.as_tuple()))

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __repr__(self):
        return "PluginId{!r}".format(self.as_tuple())


class PythonPluginStub(object):
    """An object representing a python plugin description.

    Python plugin descriptions are represented as a '__plugin__.py' file in the plugin directory.
    """
    def __init__(self, directory, plugin_id):
        """Attempts to load a python description from the directory given."""
        # TODO(Mason): Exception for plugin file not found
        self.directory = directory
        self.abs_directory = os.path.abspath(directory)
        self._py_module_filename = os.path.join(directory, "__plugin__.py")

        self._init_module()
        self._init_required(plugin_id)

    @classmethod
    def contains_stub_file(cls, directory):
        """Returns true if the directory contains a potential python plugin description."""
        return os.path.exists(os.path.join(directory, "__plugin__.py"))

    def _init_module(self):
        with open(self._py_module_filename) as module_file:
            # TODO(Mason): Exception for failure to load
            # TODO(Mason): Exception for missing plugin
            # TODO(Mason): Figure out name variable
            self._module = imp.load_module("test", module_file, self._py_module_filename, ('.py', 'r', imp.PY_SOURCE))
            self._plugin = getattr(self._module, "plugin")

    class PluginDescriptionError(PluginError): pass
    class PluginDescriptionKeyError(PluginDescriptionError): pass

    def _init_required(self, file_pid):
        desc_pid = PluginId(self.get("namespace"), self.get("version"), self.get("implementation_name"))
        if not desc_pid.compatible(file_pid):
            raise PluginDescriptionError("Plugin location name and plugin description do not match.")

        self.id = desc_pid.merge(file_pid)

        self.language = self._excepting_get("language")

        depends = self.get("depends")
        self.depends = []

        for dep in depends:
            try:
                self.depends.append(PluginId.parse(dep))
            except PluginId.NotAPluginIdString:
                pass # TODO(Mason): Resuming error messages

        imports = self.get("imports")
        self.imports = []

        for imp in imports:
            try:
                self.imports.append(PluginId.parse(imp))

            except PluginId.NotAPluginIdString:
                pass # TODO(Mason): Resuming error messages

        self.requries = self.depends + self.imports

    def init_depends(self, system):
        self.loaded_depends = []
        self.loaded_imports = []


        for dep in self.depends:
            self.loaded_depends.append(system.get_plugin(dep))

        for imp in self.imports:
            self.loaded_imports.append(system.get_plugin(imp))

        self.loaded_requires = self.loaded_depends + self.loaded_imports

        self.description = pyMDL.plugin.PluginDescription(self.get("declarations"), self.get("variables"), dict((d.id.namespace,d) for d in self.loaded_depends))

    def _excepting_get(self, name):
        v = self.get(name)
        if v is None:
            raise PluginDescriptionKeyError()
        return v

    def get(self, name):
        """Gets an arbitrary value from the loaded plugin file."""
        return (getattr(self._plugin, name) if hasattr(self._plugin, name) else None)

    def get_plugin_id(self):
        """Returns the PluginId described by the description file."""
        return PluginId(self.namespace, self.version, self.implementation_name)

class PluginDirectory(object):
    """Represents a directory potentially containing numerous plugins, which are assummed to follow canonical naming standards.

    Load the description for each plugin and validates it against it's location in the directory.
    """
    def __init__(self, system, directory, sub_namespace):
        self.system = system
        self.directory = directory
        self.sub_namespace = sub_namespace

        self._plugin_stubs = {}

        self._init_plugins()

    def _add_plugin_stub(self, plugin_stub):
        self._plugin_stubs[plugin_stub.id] = plugin_stub
        self.system._add_plugin_stub(plugin_stub)

    def _init_plugins(self):
        for root, dirs, files in os.walk(self.directory):
            relroot = os.path.relpath(root, self.directory)
            splitrelroot = relroot.split(os.sep)

            for d in splitrelroot:
                if d.startswith('.'):
                    continue

            if PythonPluginStub.contains_stub_file(root):
                file_pid = PluginId.parse(".".join(splitrelroot))
                stub = PythonPluginStub(root, file_pid)

                self._add_plugin_stub(stub)

