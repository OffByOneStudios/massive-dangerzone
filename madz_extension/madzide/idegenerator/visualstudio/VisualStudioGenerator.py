"""madzide:madzide/idegenerator/visualstudio/VisualStudioGenerator.py
@OffbyOne Studios 2014
Interface for generating ide project files.
"""

import os

import madz.module as module
from madz.bootstrap import *

from madzide.idegenerator.core.IIdeGenerator import IIdeGenerator

from . import solution_generator
from . import project_generator
from . import batch_generator
from . import filter_generator
from . import user_generator

@bootstrap_plugin("madzide.idegenerator.visualstudio")
class VisualStudioSolutionGenerator(IIdeGenerator):
    """Class which generates the visual studio solution."""


    def __init__(self, user_config):
        self.user_config = user_config

    def idegenerator_identity(self):
        return "visualstudio"

    def idegenerator_generate(self, output_dir, client_script):

        # Ensure target directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


        # Generate components
        solution = solution_generator.generate(solution_name, sln_guid, vcxproj_guid)
        project = project_generator.generate(self.user_config, solution_name, vcxproj_guid)
        user_file = user_generator.generate(client_script)
        batch_files = batch_generator.generate(client_script)
        filters = filter_generator.generate()

        with open(os.path.join(output_dir, "{}.sln".format(solution_name)), "w") as f:
            f.write(solution)

        with open(os.path.join(output_dir, "{}.vcxproj".format(solution_name)), "w") as f:
            f.write(project)

        with open(os.path.join(output_dir, "{}.vcxproj.user".format(solution_name)), "w") as f:
            f.write(user_file)

        for i in range(len(batch_files)):
            with open(os.path.join(output_dir, ["build.bat", "clean.bat", "rebuild.bat"][i]), "w") as f:
                f.write(batch_files[i])

        with open(os.path.join(output_dir, "{}.vcxproj.filters".format(solution_name)), "w") as f:
            f.write(filters)

sln_guid = "8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942"
vcxproj_guid = "D62CCCFF-D08C-4EA7-91E3-EC89A88C22CF"
solution_name = "MadzSolution"
