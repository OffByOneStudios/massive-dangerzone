"""system.py
@OffbyOneStudios 2013
Code to create Plugin Systems
"""
import logging, copy

from .plugin import *

logger = logging.getLogger(__name__)

class PluginFilter(object):
    """Object which can filter a PluginResolvers namespaces"""

    def filter(self, namespace, reverse = False):
        pass


class IdentityPluginFilter(PluginFilter):
    """Performs default filtering"""
    def filter(self, namespace, reverse = False):
        return namespace if not reverse else return {}


class PreferDirectory(PluginFilter):
    """Filter Plugins Based off of a Directory"""
    def __init__(self, directory):
        self.directory = directory

    def filter(self, namespace, reverse = False):
        res = {}
        for key, val in namespace.items():
            for stub in val:
                if (stub.directory == self.directory  and not reverse) or (stub.directory != self.directory  and reverse):
                    if not (key in res):
                        self.namespaces[key] = []
                    res[key].append(stub)
        return res


class NamespaceFilter(PluginFilter):
    """Filters Plugins Based off of Namespace Matching"""

    def __init__(self, namespace):
        self.namespace = namespace

    def filter(self, namespace, reverse=False):
        if not reverse:
            return namespace[self.namespace]
        else:
            tmp = copy.copy(namespace)
            del(tmp[self.namespace])
            return tmp


class VersionFilter(PluginFilter):
    """Filter plugins based on version number"""
    def __init__(self, version):
        self.version = version

    def filter(self, namespace, reverse = False):
        res = {}
        for key, val in namespace.items():
            for stub in val:
                if (stub.id.version == self.version  and not reverse) or (stub.id.version != self.version  and reverse):
                    if not (key in res):
                        self.namespaces[key] = []
                    res[key].append(stub)
        return res


class ImplementationFilter(PluginFilter):
    def __init__(self, implementation):
        self.implementation = implementation

    def filter(self, namespace, reverse = False):
        res = {}
        for key, val in namespace.items():
            for stub in val:
                if (stub.id.implementation_name == self.implementation  and not reverse) or (stub.id.implementation_name != self.implementation and reverse):
                    if not (key in res):
                        self.namespaces[key] = []
                    res[key].append(stub)
        return res


class PluginResolver(object):
    """Class to lookup PluginSystems based on namespaces"""
    def __init__(self):
        self.namespaces = {}
        self.plugin_stubs = set()

    def add_plugin_stub(self, plugin_stub):
        """Add Plugin Stub to system.

        Args:
            plugin_stub: plugin.PythonPluginStub object
        """
        self.plugin_stubs.add(plugin_stub)

        namespace = plugin_stub.id.namespace
        if not (namespace in self.namespaces):
            self.namespaces[namespace] = []

        self.namespaces[namespace].append(plugin_stub)

    def get_plugin(self, namespace):
        """Get Plugin by namespace.

        Args:
            namespace : String namespace of plugin

        Returns:
            plugin.PythonPluginStub object
        """
        return self.namespaces[namespace][0]

    def get_plugin_with_filter(self, namespace, the_filter, reverse=False):
        tmp = the_filter.filter(namespace, reverse)
        return tmp[namespace][0]


class PluginSystem(object):
    """ A plugin system object which manages a root namespace of objects.

    Responsible for compiling togeather and then loading plugins across language boundries.

    Attributes:
        rootname : # TODO(mason) what is this
        directories List of directories attached to plugin
        pluginstubs List of plugin.PythonPluginStub objects
    """
    def __init__(self, rootname):
        """Constructor for PluginSystem.

        Args:
            rootname: Does nothing
        """
        self.rootname = rootname
        self.directories = []
        self.plugin_stubs = []

        self.plugin_resolver = PluginResolver()

    @staticmethod
    def _join_namespaces(first, second):
        """Helper method to join namespaces.

        Args:
            First : String name of first namespace
            Second: String name of second namespace

        returns:
            String of join namespaces, delinated by '.'
        """
        splitfirst = first.split('.')
        splitsecond = second.split('.')

        return ".".join(splitfirst + splitsecond)

    def _add_plugin_stub(self, plugin_stub):
        """Add plugin_stub to plugin resolver.

        Args:
            plugin_stub: plugin.PythonPluginStub object to add
        """
        self.plugin_stubs.append(plugin_stub)
        self.plugin_resolver.add_plugin_stub(plugin_stub)

    def get_plugin(self, namespace):
        """Retrieve plugin by namespace.

        Args:
            namespace: String name of plugin.

        Returns:
            plugin.PythonPluginStub object associated with namespace
        """
        return self.plugin_resolver.get_plugin(namespace)

    def load_plugin_directory(self, directory, sub_namespace=""):
        """Load directory of plugin into memory.

        Args:
            directory: String pathname of plugin
            sub_namespace: # TODO(Mason) What is this?
        """
        self.directories.append(PluginDirectory(self, directory, sub_namespace))

    def _init_plugin(self, plugin):
        resolve_func = lambda id: self.plugin_resolver.get_plugin(id.namespace)

        if not(plugin.inited):
            for dep_id in plugin.depends:
                self._init_plugin(resolve_func(dep_id))

            if not plugin.init_requires(resolve_func):
                logger.error("Plugin {} failed to load.".format(plugin.id))
            plugin.inited = True

    def init_plugins(self):
        """Initilize Plugins."""
        for plugin in self.plugin_stubs:
            self._init_plugin(plugin)


