"""madzide:madz/ide/generator/IGenerator.py
@OffbyOne Studios 2014
Interface for generating ide project files.
"""

from abc import *

from madz.bootstrap import *


class IGenerator(metaclass=ABCMeta):
    """Class which generates the visual studio solution."""

    @abstractmethod
    def generate(self, output_dir):
        pass

    @property
    @abstractmethod
    def identity(self):
        pass
