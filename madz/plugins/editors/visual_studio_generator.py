
from ...fileman import Directory

"""visual_studio_generator.py

Functionality to generate a visual studio solution for a madz project
"""

sln_guid = "8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942"
vcxproj_guid = "D62CCCFF-D08C-4EA7-91E3-EC89A88C22CF"
solution_name = "CraftEngine"

# Template for the .sln file.
solution_template =\
"""
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio 2013
VisualStudioVersion = 12.0.21005.1
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{{solution_guid}}}") = "{solution_name}", "{solution_name}.vcxproj", "{{{vcxproj_guid}}}"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
{executable_pre_solution}
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
{executable_post_solution}
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
EndGlobal

"""

class VisualStudioSolutionGenerator(object):
    """Class which generates the visual studio solution."""

    def __init__(self, solution_name, system, output_file):
        self.system = system
        self.output_file = output_file
        self.sln_guid = "8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942"
        self.vcxproj_guid = "D62CCCFF-D08C-4EA7-91E3-EC89A88C22CF"
        self.solution_name = solution_name

    def executable_pre_solution(self, executable_name):
        """Generate a presolution declaration for a given executable name"""
        template = \
"""		Debug {executable_name}|Win32 = Debug {executable_name}|Win32\n"""

        return template.format(**{"executable_name" : executable_name})

    def executable_post_solution(self, project_guid, executable_name):
        template = \
"""		{{{vcxproj_guid}}}.Debug {executable_name}|Win32.ActiveCfg = Debug {executable_name}|Win32\n"""
        return template.format(**{"vcxproj_guid" : project_guid, "executable_name" : executable_name})

    def generate(self):
        fragments = {
            "solution_guid" : self.sln_guid,
            "vcxproj_guid" : self.vcxproj_guid,
            "solution_name" : self.solution_name,
            "executable_pre_solution" : "",
            "executable_post_solution" : "",
        }

        plugins = list(self.system.all_plugins())
        for plugin in plugins:
            if plugin.executable:
                # Fill in executables in solution
                fragments["executable_pre_solution"] += self.executable_pre_solution(plugin.id.namespace)
                fragments["executable_post_solution"] += self.executable_post_solution(self.vcxproj_guid, plugin.id.namespace)

        with open(self.output_file, "w") as f:
            f.write(solution_template.format(**fragments))