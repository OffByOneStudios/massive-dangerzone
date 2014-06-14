import abc
import os
import subprocess
import logging

from . import compiler
from ...module.dependency import Dependency

logger = logging.getLogger(__name__)

class SubprocCompilerBase(compiler.BaseCompiler):
    """A compiler object which uses subprocesses to perform compilation steps (as opposed to direct calls)."""
    def __init__(self, language):
        compiler.BaseCompiler.__init__(self, language)

    class OperationType():
        """Class used to assign key values to compiler operation types."""
        Compile = 0
        Link = 1

    @abc.abstractmethod
    def file_extension_binary_object(self):
        """The string representing the file extension for binary objects."""
        pass

    @abc.abstractmethod
    def binary_name_binary_compiler(self):
        """The string representing the name of the binary which can compile the binary."""
        pass

    @abc.abstractmethod
    def binary_name_shared_linker(self):
        """The string representing the name of the linker which can compile the shared plugin."""
        pass

    @abc.abstractmethod
    def args_binary_compile(self, source_file):
        """Generates a string, which, when executed, will turn the source file into an object file.

        The binary file need only be applicable to this linker.
        """
        pass

    @abc.abstractmethod
    def args_shared_link(self, object_files):
        """Generates a string, which, when executed, will turn the object files into a shared object.

        The generated object should be appropriate for the operating system.
        """
        pass

    @abc.abstractmethod
    def log_output(self, operation, retcode, output, errput):
        #TODO(Mason): Implement this method and add proper descriptions of input paramaters.
        """Responsible for logging the output from the proccess.

        Args:
            operation:
            retcode:
            output:
            errput:
        """
        pass

    def _prep(self):
        pass

    def _run_subprocess(self, name, dir, args):
        args = list(map(str, args))
        logger.debug("Running command:\n\t\t{}".format(" ".join(args)))

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

        #Ask compilers to determine whether output needs to be logged
        self.log_output(retcode, output, errput, foutput, ferrput)

    def build(self, type=compiler.BaseCompiler.BuildType.DynamicPlugin):
        """Compiles and links plugin.

        Implementation Notes:
            Hard Coded to use GCC
            Links as Unix Style Shared Objects.
        """
        self._prep()

        self.language.build_directory.require()

        source_files = self.language.get_source_files()
        source_files += self.language.get_internal_source_files()

        for sf in source_files:
            self._run_subprocess(name="Compile: \"{}\"".format(sf),
                args=self.args_binary_compile([sf]),
                dir=str(self.language.build_directory))

        object_files = map(lambda c: c
                .with_extension(self.file_extension_binary_object()[1:])
                .with_directory(self.language.build_directory),
            source_files)

        self.language.output_directory.require()

        self._run_subprocess(name="Link: \"{}\"".format(self.language.get_output_file()),
            args=self.args_shared_link(object_files),
            dir=self.language.build_directory.as_string())

    def get_dependency(self):
        """Returns a dependency object for this operation."""
        targets = [self.language.get_output_file()]
        dependencies = list(self.language.get_source_files())
        dependencies.extend(self.language.get_internal_source_files())
        return Dependency(dependencies, targets)

