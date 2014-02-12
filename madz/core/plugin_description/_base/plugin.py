"""core/plugin_description/_base/plugin.py
@OffbyOneStudios 2013
Basic plugin description object.
"""

from ....config import plugin as plugin_config # for PluginConfig defaults
from ....MDL import loaders
from ....MDL import base_types

class HumanMDLLoader(loaders.IMdlLoader):
    def __init__(self, nodes):
        self.ast = self._transform_ast_named_strs(nodes)

    def _map_over(self, ast, map_func):
        """Applies a map function over this nodes subnodes.
        
        Args:
            map_func: A map function to be applied across the node.
            ast: List of subnodes,
        
        Returns:
            The subnodes after having the map function applied to it.
        """
        new_ast = []
        for node in ast:
            new_subs = map_func(node)
            for new_sub_node in new_subs:
                new_ast.append(new_sub_node.map_over(map_func))
        return new_ast
        
    def _transform_ast_named_strs(self, ast):
        """Names each subnode of the description.
        
        Args:
            ast: List of subnodes
            
        Returns:
            The MDLDescription object with named subnodes.
        """
        
        def str_to_named(node, name=""):
            ret_node = node
            if isinstance(node, str):
                ret_node = base_types.NamedType(node)
            if name:
                return [(name, ret_node)]
            return [ret_node]

        return self._map_over(ast, str_to_named)

    def load(self, dir=""):
        return self.ast


class PluginDescription(object):
    """Object Containing description of Plugins.

    Takes **kwargs of the following

    Attributes:
        name: String representing the fully qualified name of plugin
        version: String or SemanticVersion representing  version of plugin
        implementation: String representing the name of the particular implementation of the plugin
        language: String representing the language the plugin is written in.
        libraries: List of libraries used by the plugin.
        config: A PluginConfig object representing the configuration for the plugin.
        imports: Strings or [Partial]PluginIds representing the plugins that this plugin makes use of.
        depends: Strings or [Partial]PluginIds representing the plugins that this plugin uses in it's description as well as potential makes use of.
        description: The MDL description of what the plugin provides.
        active: A way to disable the plugin before it hits the system.
        documentation: A String describing the plugin. The first line should be a short blurb, folowed by a blank line, and then the full description.
    """

    def __init__(self, **kwargs):
        self._args = kwargs

        def init_get(key, default=None):
            return self._args.get(key, default)

        self.name = init_get("name")
        self.version = init_get("version")
        self.implementation = init_get("implementation")

        self.language = init_get("language")
        self.libraries = init_get("libraries", [])

        self.platform_check = init_get("platform_check", lambda p: True)

        self.config = init_get("config", plugin_config.PluginConfig())

        self.active = init_get("active", True)
        self.imports = init_get("imports",[])
        self.depends = init_get("depends",[])

        desc = init_get("description",[])
        if isinstance(desc, loaders.IMdlLoader):
            self.description = loaders.MdlCachedLoader(desc)
        elif isinstance(desc, str):
            self.description = loaders.MdlCachedLoader(loaders.MdlStringLoader(desc))
        elif isinstance(desc, list):
            self.description = HumanMDLLoader(desc)
        else:
            raise TypeError("Invalid Description Type")
        
        self.doc = init_get("documentation", "")
