"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys
import subprocess

from madz.dependency import Dependency

class Builder(object):
    """Object Which can build C plugins.

    Attributes:
        plugin_stub madz.plugin.PythonPluginStub object
    """
    def __init__(self, language):
        """Constructor for C Builder.

        Args:
            plugin_stub madz.plugin.PythonPluginStub object
        """
        self.language = language
        self.compiler = language.get_compiler()
        self.plugin_stub = language.plugin_stub

    def prep(self):
        """Performs any pre-compile stage prep work for plugin."""
        if not (os.path.exists(self.language.get_build_directory())):
            os.makedirs(self.language.get_build_directory())

        if not (os.path.exists(self.language.get_output_directory())):
            os.makedirs(self.language.get_output_directory())

    def run_subprocess(self, dir, args):
        compile_process = subprocess.Popen(
            args,
            cwd=dir,
            stdout=subprocess.PIPE)
        return compile_process.stdout.read()

    def build(self):
        """Compiles and links plugin.

        Implementation Notes:
            Hard Coded to use GCC
            Links as Unix Style Shared Objects.
        """
        self.prep()

        source_files = self.language.get_c_source_files()
        source_files.append(self.language.get_c_code_filename())

        print "*** => COMPILE"
        print self.run_subprocess(
            args=self.compiler.args_compile(source_files),
            dir=self.language.get_build_directory())

        object_files = map(lambda c: os.path.basename(c)[:-2] + ".o", source_files)

        print "*** => LINK"
        print self.run_subprocess(
            args=self.compiler.args_link(object_files),
            dir=self.language.get_build_directory())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [self.language.get_output_file()]
        dependencies = self.language.get_c_source_files()
        dependencies.append(self.language.get_c_code_filename())
        return Dependency(dependencies, targets)

