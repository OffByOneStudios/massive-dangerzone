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
        implementation_name: A string representing the unique implementation name.
    """
    def __init__(self, namespace, version, implementation_name="default"):
        self.namespace = namespace
        self.version = version
        self.implementation_name = implementation_name

    class PluginIdParseError(Exception): pass

    @classmethod
    def parse(cls, relative):
        """Parses a canoical plugin id string into a PluginIndex"""
        if isinstance(relative, cls):
            return relative

        relativestring = relative

        version_string = None
        version_start = relativestring.find('[')
        version_end = relativestring.find(']')
        if (version_start == -1) ^ (version_start == -1):
            raise PluginIdParseError("Cannot contain ']' or '[' except as version delimiters.")
        elif version_start != -1:
            version_string = relativestring[version_start+1:version_end]
            relativestring = relativestring[:version_start] + relativestring[version_end+1:]

        implname_string = None
        implname_start = relativestring.find('(')
        implname_end = relativestring.find(')')
        if (implname_start == -1) ^ (implname_start == -1):
            raise PluginIdParseError("Cannot contain ')' or '(' except as version delimiters.")
        elif implname_start != -1:
            implname_string = relativestring[implname_start+1:implname_end]
            relativestring = relativestring[:implname_start] + relativestring[implname_end+1:]

        relativestring = relativestring.strip(".")

        return cls(relativestring, SemanticVersion.parse(version_string), implname_string)

    def as_tuple(self):
        """Returns a tuple for uniquely indentifying the PluginIndex"""
        return (self.namespace, self.version, self.implementation_name)

    def __hash__(self):
        return hash(self.as_tuple())

    def compatible(self, other):
        return \
            functools.reduce(lambda a, i: a and i,
                map(lambda a, b: a == b or ((a is None) != (b is None)),
                    self.as_tuple(), other.as_tuple()))

    def merge(self, other):
        return PluginId(*map(lambda a, b: a or b, self.as_tuple(), other.as_tuple()))

    def __eq__(self, other):
        return self.as_tuple() == other.as_tuple()

    def __repr__(self):
        return "PluginId{!r}".format(self.as_tuple())

class PartialPluginId(PluginId):
    """Represents a plugin id which can refrence more than a single plugin."""
    #TODO:
    pass

