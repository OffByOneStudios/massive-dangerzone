from plugin import *

class PluginResolver(object):
    def __init__(self):
        self.namespaces = {}
        self.plugin_stubs = set()

    def add_plugin_stub(self, plugin_stub):
        self.plugin_stubs.add(plugin_stub)

        namespace = plugin_stub.id.namespace
        if not (namespace in self.namespaces):
            self.namespaces[namespace] = []

        self.namespaces[namespace].append(plugin_stub)

    def get_plugin(self, namespace):
        return self.namespaces[namespace][0]
        

class PluginSystem(object):
    """ A plugin system object which manages a root namespace of objects.

    Responsible for compiling togeather and then loading plugins across language boundries.

    """
    def __init__(self, rootname):
        self.rootname = rootname
        self.directories = []
        self.plugin_stubs = {}

        self.plugin_resolver = PluginResolver()

    @staticmethod
    def _join_namespaces(first, second):
        splitfirst = first.split('.')
        splitsecond = second.split('.')

        return ".".join(splitfirst + splitsecond)

    def _add_plugin_stub(self, plugin_stub):
        self.plugin_stubs[plugin_stub.id] = plugin_stub
        self.plugin_resolver.add_plugin_stub(plugin_stub)

    def get_plugin(self, namespace):
        return self.plugin_resolver.get_plugin(namespace)

    def load_plugin_directory(self, directory, sub_namespace=""):
        self.directories.append(PluginDirectory(self, directory, sub_namespace))

