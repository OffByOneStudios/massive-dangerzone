"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys
import subprocess

import shared

from madz.dependency import Dependency

class Builder(object):
    """Object Which can build C plugins.

    Attributes:
        plugin_stub madz.plugin.PythonPluginStub object
    """
    lang = shared.LanguageShared

    def __init__(self, plugin_stub):
        """Constructor for C Builder.

        Args:
            plugin_stub madz.plugin.PythonPluginStub object
        """

        self.plugin_stub = plugin_stub
        self._s_dir = self.plugin_stub.abs_directory
        self._b_dir = self.lang.get_build_directory(self.plugin_stub)
        self._w_dir = self.lang.get_wrap_directory(self.plugin_stub)
        self._o_dir = self.lang.get_output_directory(self.plugin_stub)

    def prep(self):
        """Performs any pre-compile stage prep work for plugin."""
        if not (os.path.exists(self._b_dir)):
            os.makedirs(self._b_dir)

        if not (os.path.exists(self._o_dir)):
            os.makedirs(self._o_dir)

    def subprocess_list_c_compile(self):
        return ["gcc", "-c", "-I"+shared.LanguageShared.get_wrap_directory(self.plugin_stub), "-fpic"]

    def build_c_files(self, filenames):
        compile_process = subprocess.Popen(
            self.subprocess_list_c_compile() + filenames,
            cwd=self._b_dir,
            stdout=subprocess.PIPE)
        return compile_process.stdout.read()

    def build(self):
        """Compiles and links plugin.

        Implementation Notes:
            Hard Coded to use GCC
            Links as Unix Style Shared Objects.
        """
        self.prep()

        source_files = []
        for f in os.listdir(self._s_dir):
            if os.path.isfile(os.path.join(self._s_dir, f)) and f.endswith(".c"):
                source_files.append(os.path.join("..", f))
        source_files.append(self.lang.get_c_code_filename(self.plugin_stub))

        print "*** => COMPILE"
        print self.build_c_files(source_files)

        object_files = map(lambda c: os.path.basename(c)[:-2] + ".o", source_files)

        out_link = subprocess.Popen(
            ["gcc", "-shared", "-o", os.path.join(self._o_dir, self.plugin_stub.id.namespace + ".madz")] + object_files,
            cwd=self._b_dir,
            stdout=subprocess.PIPE)
        print "*** => LINK"
        print out_link.stdout.read()

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [os.path.join(self._o_dir, self.plugin_stub.id.namespace + ".madz")]
        dependencies = self.lang.get_c_files_from(self.plugin_stub)
        dependencies.append(self.lang.get_c_code_filename(self.plugin_stub))
        return Dependency(dependencies, targets)

