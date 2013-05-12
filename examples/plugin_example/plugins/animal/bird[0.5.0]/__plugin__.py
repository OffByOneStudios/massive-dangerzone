from magic.plugins import *

name = "animal.bird"
version = "0.5.0"

requires = [Interface("kingdom.animal.IAnimal")]

resolve_requirements()

from .base import BirdBase

provides = [Implementation(BirdBase)]
