"""madzide:madz/ide/generator/core/IIdeGenerator.py
@OffbyOne Studios 2014
Interface for generating ide project files.
"""


import abc

class IIdeGenerator(metaclass=abc.ABCMeta):
    """Class which generates the visual studio solution."""

    @abc.abstractmethod

    def idegenerator_generate(self, output_dir, client_script):
        """Generate an IDE's project files containing madz modules.

        Args:
            output_dir : string The absolute path to the directory where project files will be created.
            client_script : string The absolute path to the client script which is invoking this generation.

        """
        pass

    @property
    @abc.abstractmethod
    def idegenerator_identity(self):
        pass


