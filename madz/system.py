"""system.py
@OffbyOneStudios 2013
Code to create Plugin Systems
"""
import logging, copy

from .plugin import *

logger = logging.getLogger(__name__)

class PluginFilter(object):
    """Object which can filter a PluginResolvers namespaces"""
    def __init__(self, reverse=False):
        self.reverse = reverse

    def filter(self, candidates):
        pass

class PluginOrderer(PluginFilter):
    """Object which can sort a PluginResolvers namespaces"""
    def sort(self, candidates):
        pass

    def filter(self, candidates):
        return self.sort(candidates)


class LambdaFilter(PluginFilter):
    """Plugin Filter which accepts a filter function."""
    def __init__(self, fn, reverse=False):
        self.fn = (lambda a: not fn(a)) if reverse else fn
        self.reverse = reverse

    def filter(self, candidates):
        return list(filter(self.fn, candidates))


class LambdaOrderer(PluginOrderer):
    """Plugin Orderer which accepts a order function.

    Attributes:
        fn : Function which returns a comparable object from the incoming collection
            defaults to identity
    """
    def __init__(self, fn=lambda a:a, reverse=False):
        self.fn = fn

    def sort(self, candidates):
        return sorted(candidates, key=self.fn)


class IdentityPluginFilter(LambdaFilter):
    """Performs default filtering"""
    def __init__(self, reverse=False):
        self.fn = (lambda a: False) if reverse else (lambda a: True)


class DirectoryFilter(LambdaFilter):
    """Filter Plugins Based off of a Directory"""
    def __init__(self, directory, reverse=False):
        self.directory = directory
        self.reverse = reverse
        self.fn = lambda a: ((a.directory == self.directory) != reverse)


class ImplementationFilter(LambdaFilter):
    def __init__(self, implementation, reverse=False):
        self.implementation = implementation
        self.reverse = reverse
        self.fn = lambda a: (self.implementation == a.id.implementation_name) != reverse


class NamespaceFilter(LambdaFilter):
    def __init__(self, namespace, reverse=False):
        self.namespace = namespace
        self.reverse = reverse
        self.fn = lambda a: (self.namespace == a.id.namespace) != reverse


class VersionFilter(LambdaFilter):
    """Filter plugins based on version number"""
    eq="eq"
    gt="gt"
    lt="lt"
    lteq="lteq"
    gteq="gteq"
    neq="neq"
    comparators = [eq, gt, lt, lteq, gteq, neq]

    def __init__(self, version, reverse=False, op=eq):
        self.version = version
        self.reverse = reverse
        self.fn =self._cmp(op)

    def _cmp(self, other_version):
        if self.op == self.eq:
            return lambda a:((a.id.other_version == self.version) != self.reverse)
        elif self.op == self.gt:
            return lambda a:((a.id.other_version > self.version) != self.reverse)
        elif self.op == self.lt:
            return lambda a:((a.id.other_version < self.version) != self.reverse)
        elif self.op == self.gteq:
            return lambda a:((a.id.other_version >= self.version) != self.reverse)
        elif self.op == self.lteq:
            return lambda a:((a.id.other_version <= self.version) != self.reverse)
        else:
            return lambda a:((a.id.other_version != self.version) != self.reverse)


class VersionOrderer(LambdaOrderer):
    def __init__(self, reverse=False):
        self.fn = lambda a: a.id.version


class PluginResolverException(Exception):
    pass


class PluginResolver(object):
    """Class to lookup PluginSystems based on namespaces"""
    def __init__(self):
        self.namespaces = {}
        self.plugin_stubs = set()
        self.filters = [IdentityPluginFilter()]

    def add_filter(self, filter, index=None):
        if index == None:
            self.filters.append(filter)
        else:
            self.filters[index] = filter

    def _get_plugin(self, namespace):
        """Get Plugin by namespace.

        This private method wrap access into the namespace dictionary to manage aliases.

        Args:
            namespace : String namespace of plugin

        Returns:
            plugin.PythonPluginStub object
        """
        try:
            if isinstance(self.namespaces[namespace],list):
                return self.namespaces[namespace]
            elif isinstance(self.namespaces[namespace], str):
                return self.namespaces[self.namespaces[namespace]]
        except KeyError:
            logger.error("Namespace:{} not found.".format(namespace))
            raise PluginResolverException("Namespace:{} not found.".format(namespace))

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

    def alias(self, alias_name, namespace):
        """Alias a namespace.

        Args:
            alias_name: string name of new namespace to create
            namespace: string name of old namespace to point to

        Returns:
            None

        Raises:
            PluginResolverException if alias_name already exists
        """
        if alias_name in self.namespaces:
            raise PluginResolverException("Cannot alias Namespace:{}. Namespace already exists.".format(namespace))
        self.namespaces[alias_name] = namespace

    def get_plugin(self, namespace):
        candidates = self._get_plugin(namespace)
        for fil in self.filters:
            candidates = fil.filter(candidates)
            if candidates == []:
                raise PluginResolverException("No candidates match query:{} for filters {}".format(namespace,self.filters))

        return candidates[0]

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


