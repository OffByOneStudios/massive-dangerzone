"""core/plugin_stub.py
@OffbyOne Studios 2013
Contains the PluginStub object which represents plugins.
"""

import os, sys
import imp
import logging
import traceback
import contextlib

from .plugin_id import *
from ..config import *

from .. import language

from ..MDL import description as pyMDL

logger = logging.getLogger(__name__)

class PluginError(Exception): pass

class PluginStub(object):
    """An object representing a python plugin description.

    Python plugin descriptions are represented as a '__plugin__.py' file in the plugin directory.

    Attributes:
        directory: The directory containing the plugin.
        abs_directory: An absolute version of directory.
        id: The PluginId object representing this plugin.
        language: The programming language of this plugin.
        depends: The PluginId's of plugins this one's description depends on.
        imports: The PluginId's of plugins this one uses in it's implementation.
        requires: Both depends and imports.
        inited: False untill init_requires is called.
        loaded_depends: The plugins corresponding to depends. (Monkeypatched by init_requires)
        loaded_imports: The plugins corresponding to imports. (Monkeypatched by init_requires)
        loaded_requires: The plugins corresponding to requires. (Monkeypatched by init_requires)
        description: Contains a PluginDescription object wrapping the MDL for this plugin. (Monkeypatched by init_requires)
    """
    def __init__(self, system, plugin_description_loader, plugin_id):
        """Attempts to load a python description from the directory given."""
        # TODO(Mason): Exception for plugin file not found
        self.system = system
        self.directory = plugin_description_loader.get_directory()
        self._plugin = plugin_description_loader.get_plugin_description()
        self._plugin_loader_files = plugin_description_loader.get_plugin_loader_files()

        self._init_description(plugin_id)

        self.inited = False

    def __str__(self):
        return "<PluginStub: {!s}>".format(self.id)

    def __repr__(self):
        return "<PluginStub: {!r}>".format(self.id)

    class PluginDescriptionError(PluginError): pass
    class PluginDescriptionKeyError(PluginDescriptionError): pass

    def _get(self, name):
        """Gets an arbitrary value from the loaded plugin file."""
        try:
            return getattr(self._plugin, name)
        except Exception as exc:
            raise PluginDescriptionKeyError() from exc

    def _try_get(self, name, default=None):
        """Attempts to call _get. Returns default if it cannot."""
        try:
            return self._get(name)
        except:
            return default

    def _init_description(self, file_pid):
        """Called in __init___, helper to initialize the Plugin Stub."""
        # Determine the plugin id from the description file:
        desc_pid = PluginId(
            self._try_get("namespace"),
            SemanticVersion.parse(self._try_get("version")),
            self._try_get("implementation_name"))

        # Verify the plugin id from the file name and description file are compatible
        if not desc_pid.compatible(file_pid):
            raise PluginDescriptionError("Plugin location name and plugin description do not match.")

        # Save the merged plugin id
        self.id = desc_pid.merge(file_pid)

        # Get language stuff:
        self.language_name = self._get("language")
        self.language_module = language.get_language(self.language_name)

        self.libraries = self._get("libraries")

        # Save the plugin specific configs
        # These merges must obey config load order:
        # * Default language config base incase no other config is available
        # * System config contains the correct order for: Default -> User -> System
        # * Plugin config is the config from the plugin descriptions
        self.config = self._try_get("config")

        # Build and save the language object for the plugin
        with config.and_merge(self.config):
            self.language = self.language_module.Language(self)

        # Initialize depends names:
        depends = self._try_get("depends")
        self.depends = []
        for dep in depends:
            try:
                self.depends.append(PluginId.parse(dep))
            except PluginId.NotAPluginIdString:
                pass # TODO(Mason): Resuming error messages

        # Initialize imports names:
        imports = self._try_get("imports")
        self.imports = []
        for imp in imports:
            try:
                self.imports.append(PluginId.parse(imp))
            except PluginId.NotAPluginIdString:
                pass # TODO(Mason): Resuming error messages

        # Build requirements names
        self.requires = self.depends + self.imports

    def check_platform(self, target_platform):
        """Calls the check platform function, if one does not exist returns false."""
        return self._try_get("platform_check", lambda p: False)(target_platform)

    def init_requires(self, lookup_func):
        """This initalizes the requires into *_loaded variables by finding the concrete PluginStub objects. Also validates the MDL.

        This monkeypatches the object with new variables."""
        # New empty mokey-pached variable.
        self.loaded_depends = []
        self.loaded_imports = []

        # Lookup loaded depends and imports
        for dep in self.depends:
            self.loaded_depends.append(lookup_func(dep))
        for imp in self.imports:
            self.loaded_imports.append(lookup_func(imp))

        # Construct loaded requires
        self.loaded_requires = self.loaded_depends + self.loaded_imports

        # Build and save the plugin's MDL:
        with config.and_merge(self.config):
            ast = self._try_get("description")
            ast = pyMDL.MDLDescription.transform_ast_user_convenience(ast)
            self.description = pyMDL.MDLDescription(ast, 
                dict((d.id.namespace, d.description) for d in self.loaded_depends),
                dir=self.directory)

        # Validate the plugin description, and use it's return as whether we succeded or not.
        return self.description.validate()

    @contextlib.contextmanager
    def and_configs(self):
        """"""
        # Copy state to restore later
        old_state = config.copy_state()

        # Merge in this plugin's config
        with config.and_merge(self.config):
            # Generate the config to pull the lib configs from (speed and safety)
            config_for_libs = config.get_merged_config()

            # Add the library configs
            for library in self.libraries:
                config.add(config_for_libs.get_option(LibraryConfig.make_key(library)))

            # Merge in the language's config
            with config.and_merge(config.get_option(LanguageConfig.make_key(self.language_name))):
                yield

        # Safely restore the config object
        config.set_state(old_state)

    def gen_recursive_loaded_depends(self):
        """Generates a list of all dependencies. In orderish."""
        
        # new list to return
        new_list = []
        for dep in self.loaded_depends:
            # inspect recursive subdepends for depends candidates 
            subdeps = dep.gen_recursive_loaded_depends()
            for subdep in subdeps:
                # Add new dependencies 
                if not(subdep in new_list):
                    new_list.append(subdep)
            # Add this plugin's depedencies.
            if not(dep in new_list):
                new_list.append(dep)
                
        return new_list

    def gen_required_loaded_imports(self):
        """Generates a list of all imports. In orderish."""
        imports_list = []
        for plugin_import in self.loaded_imports:
            if plugin_import not in imports_list:
                for p in plugin_import.gen_recursive_loaded_depends():
                    if p not in imports_list:
                        imports_list.append(p)
                imports_list.append(plugin_import)
        return imports_list

    def gen_recursive_loaded_requires(self):
        """Generates a list of all requirements. No order."""
        requires_list = []
        new_list = self.loaded_requries
        while not (len(new_list) == 0):
            requires_list.extend(new_list)
            new_list = []
            for lreq in requires_list:
                for lreqreqs in lreq.loaded_requries:
                    if not (lreqreqs in requires_list or lreqreqs in new_list):
                        new_list.append(lreqreqs)
        return requires_list

    def get_plugin_id(self):
        """Returns the PluginId described by the description file."""
        return PluginId(self.namespace, self.version, self.implementation_name)


