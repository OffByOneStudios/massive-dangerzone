"""plugin_id.py
@OffbyOne Studios 2013
Contains classes which represent a plugins IDs.
"""
import functools

from .semver import *

class PluginId(object):
    """A value type for uniquely identifying plugins.

    Attributes:
        namespace: The dotted namespace.
        version: The semver version.
        implementation: A string representing the unique implementation name.
    """
    def __init__(self, namespace, version, implementation="default"):
        self.namespace = namespace
        self.version = version
        self.implementation = implementation

    class PluginIdParseError(Exception): pass

    @classmethod
    def parse(cls, relative):
        """Parses a canonical plugin id string into a PluginIndex
        
        Arguments:
            relative: A string representing a plugin ID.
        """
        if isinstance(relative, cls):
            return relative

        relativestring = relative

        # Grab the version name from the plugin id string
        version_string = None
        version_start = relativestring.find('[')
        version_end = relativestring.find(']')
        if (version_start == -1) ^ (version_start == -1):
            raise PluginIdParseError("Cannot contain ']' or '[' except as version delimiters.")
        elif version_start != -1:
            version_string = relativestring[version_start+1:version_end]
            relativestring = relativestring[:version_start] + relativestring[version_end+1:]

        # Grab the implementation name string from the plugin id string
        implname_string = None
        implname_start = relativestring.find('(')
        implname_end = relativestring.find(')')
        if (implname_start == -1) ^ (implname_start == -1):
            raise PluginIdParseError("Cannot contain ')' or '(' except as version delimiters.")
        elif implname_start != -1:
            implname_string = relativestring[implname_start+1:implname_end]
            relativestring = relativestring[:implname_start] + relativestring[implname_end+1:]

        relativestring = relativestring.strip(".")

        return cls(
            relativestring,
            SemanticVersion.parse(version_string),
            implname_string)

    def as_tuple(self):
        """Returns a tuple for uniquely identifying the PluginIndex"""
        return (self.namespace, self.version, self.implementation)

    def __hash__(self):
        return hash(self.as_tuple())

    def compatible(self, other):
        """Returns true if the PluginId is compatible with the provided PluginId, and false otherwise."""
        return \
            functools.reduce(lambda a, i: a and i,
                map(lambda a, b: ((a is None) != (b is None)) or a == b,
                    self.as_tuple(), other.as_tuple()))

    def merge(self, other):
        """Merges the PluginId with another PluginId."""
        return PluginId(*map(lambda a, b: a or b, self.as_tuple(), other.as_tuple()))

    def __eq__(self, other):
        return isinstance(other, PluginId) and self.as_tuple() == other.as_tuple()

    def __str__(self):
        return "{}{}{}".format(
            self.namespace,
            "[{!s}]".format(self.version) if not (self.version is None) else "",
            "({})".format(self.implementation) if not (self.implementation is None) else "")

    def __repr__(self):
        return "PluginId{!r}".format(self.as_tuple())

class PartialPluginId(PluginId):
    """Represents a plugin id which can reference more than a single plugin."""
    #TODO:
    pass

"""
#Example Usage of PluginId

pluginid = PluginId("the/namespace.of/plugin", "[1.0]", "implementation_name")
pluginid2 = PluginId.parse("the/namespace.of/plugin/[1.0]/(implementation_name)")

pid_tuple = pluginid.as_tuple()

if compatible(pluginid, pluginid2):
    pass

merge(pluginid, pluginid2)

if pluginid == pluginid2:
    pass

plugin_string = str(pluginid)
    
print pluginid
"""