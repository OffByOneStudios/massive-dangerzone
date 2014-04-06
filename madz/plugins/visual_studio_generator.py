


class VisualStudioSourceFile(object):
    """Class reperesenting a Source File included in a MADZ visual studio project."""
    pass


class VisualStudioClFile(VisualStudioSourceFile):
    """Class Representing a file compiled by CL (C++)"""
    pass


class VisualStudioMdlFile(VisualStudioSourceFile):
    """Class Representing a file compiled by CL (C++)"""
    pass


class VisualStudioPythonFile(VisualStudioSourceFile):
    """Class Representing a python file"""
    pass


class VisualStudioSolutionGenerator(object):
    """Class which generates the visual studio solution."""

    def __init__(self, config, system, output_file):

        self.config = config
        self.system = system
        self.output_file = output_file
        print(system)