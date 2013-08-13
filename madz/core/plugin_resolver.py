"""core/plugin_resolver.py
@OffbyOne Studios 2013
Manages plugin resolution.
"""
import logging

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
        except KeyError as exc:
            logger.error("Namespace:{} not found.".format(namespace))
            raise PluginResolverException("Namespace:{} not found.".format(namespace)) from exc

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
