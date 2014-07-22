"""subprocess_base.py
@Offbyone Studios 2014
"""

import subprocess
import logging
from abc import *

from .compiler_base import CompilerBase

logger = logging.getLogger(__name__)

class SubprocessBase(CompilerBase):

    @abstractmethod
    def process_output(self, name, retcode, output, errput, foutput, ferrput):
        """Responsible for processing the output from the proccess.
        
        Args:
            name: string name of process phase
            retcode: return code from subprocess
            output: original output
            errput: original error output
            foutput: formatted output
            ferrput: formated error output
        
        Returns:
            True if suscessfully compiled, false otherwise.
        """
        pass
    
    def invoke_simple(self, args, dir=None):
        if not dir is None:
            dir.ensure()
            path = dir.path
        else:
            path = "."
        
        compile_process = subprocess.Popen(
            args,
            cwd=path,
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
        return (retcode, output, errput)
        
    def invoke(self, name, dir, args):
        logger.debug("Running command:\n\t\t{}".format(" ".join(args)))

        retcode, output, errput = self.invoke_simple(args, dir)

        foutput = "Build Phase ({}) Out:\n\t\t{}".format(
            name, "\n\t\t".join(output.split("\n")))
        ferrput = "Build Phase ({}) Err:\n\t\t{}".format(
            name, "\n\t\t".join(errput.split("\n")))

        #Ask compilers to determine whether output needs to be logged
        return self.process_output(name, retcode, output, errput, foutput, ferrput)
