"""build.py
@OffbyOne Studios 2013
Code to Build C plugins
"""

import os, sys
import logging
import subprocess

from madz.dependency import Dependency

logger = logging.getLogger(__name__)

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

    def run_subprocess(self, name, dir, args):
        compile_process = subprocess.Popen(
            args,
            cwd=dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        cpdone = compile_process.returncode is None
        output = compile_process.stdout.read() if not cpdone else ""
        errput = compile_process.stderr.read() if not cpdone else ""
        while compile_process.returncode is None:
            tout, terr = compile_process.communicate()
            tout, terr = (str(tout.decode("utf-8")), str(terr.decode("utf-8")))
            output += tout
            errput += terr
            if str(tout) == "" and str(terr) == "":
                break

        retcode = compile_process.returncode
        foutput = "Build Phase ({}) Out:\n\t\t{}".format(
            name, "\n\t\t".join(output.split("\n")))
        ferrput = "Build Phase ({}) Err:\n\t\t{}".format(
            name, "\n\t\t".join(errput.split("\n")))

        if retcode != 0:
            if output != "":
                logger.error(foutput)
            if errput != "":
                logger.error(ferrput)
        else:
            if output != "":
                logger.warning(foutput)
            if errput != "":
                logger.warning(ferrput)


    def build(self):
        """Compiles and links plugin.

        Implementation Notes:
            Hard Coded to use GCC
            Links as Unix Style Shared Objects.
        """
        self.prep()

        source_files = self.language.get_c_source_files()
        source_files.append(self.language.get_c_code_filename())

        for sf in source_files:
            self.run_subprocess(name="Compile: \"{}\"".format(sf),
                args=self.compiler.args_compile([sf]),
                dir=self.language.get_build_directory())

        object_files = map(lambda c: os.path.basename(c)[:-2] + ".o", source_files)

        self.run_subprocess(name="Link",
            args=self.compiler.args_link(object_files),
            dir=self.language.get_build_directory())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [self.language.get_output_file()]
        dependencies = self.language.get_c_source_files()
        dependencies.append(self.language.get_c_code_filename())
        return Dependency(dependencies, targets)

