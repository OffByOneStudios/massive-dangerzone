
"""madzide:madzide/idegenerator/visualstudio/VisualStudioGenerator.py
@OffbyOne Studios 2014
Generates .sln files
"""

import madz.module as module
from madz.bootstrap import *


def generate(solution_name, solution_guid, project_guid):
    fragments = {
      "solution_guid" : solution_guid,
      "project_guid" : project_guid,
      "solution_name" : solution_name,
      "executable_post_solution" : "",
    }

    plugins = list(map(module.EcsModules.current, module.EcsModules.current[module.Old].entities()))
    for plugin in plugins:
        if plugin.old.executable:
            # Fill in executables in solution
            executable = plugin.id.namespace
            fragments["executable_post_solution"] += "\t{{{}}}.{}|Win32 = Build|Win32\n".format(project_guid, executable)

    return solution_template.format(**fragments)

solution_template =\
"""Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio 2013
VisualStudioVersion = 12.0.21005.1
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{{solution_guid}}}") = "{solution_name}", "{solution_name}.vcxproj", "{{{project_guid}}}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
    Build|Win32 = Build|Win32
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
{executable_post_solution}
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
EndGlobal

"""
