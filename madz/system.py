from plugin import *

class PluginResolver(object):
    def __init__(self):
        self.namespaces = {}
        self.plugins = set()

    def add_plugin(self, plugin_stub):
        self.plugins.add(plugin_stub)
        self.plugins[plugin_stub.namespace] = plugin_stub

    def get_plugin(self, namespace):
        pass
        

class PluginSystem(object):
    """ A plugin system object which manages a root namespace of objects.

    Responsible for compiling togeather and then loading plugins across language boundries.

    """
    def __init__(self, rootname):
        self.rootname = rootname
        self.directories = []
        self.plugin_descriptions = {}

    @staticmethod
    def _join_namespaces(first, second):
        splitfirst = first.split('.')
        splitsecond = second.split('.')

        return ".".join(splitfirst + splitsecond)

    def _add_plugin_description(self, plugin_description):
        self.plugin_descriptions[plugin_description.id] = plugin_description

    def get_plugin(self, plugin_index):
        return self.plugin_stubs[plugin_index]

    def load_plugin_directory(self, directory, sub_namespace=""):
        self.directories.append(PluginDirectory(self, directory, sub_namespace))
