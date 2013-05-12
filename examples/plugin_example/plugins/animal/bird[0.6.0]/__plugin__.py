from magic.plugins import *

name = "animal.bird"
version = "0.6.0"

requires = [Interface("kingdom.animal.IAnimal", version=VersionRange("0.1.0"))]

resolve_requirements()

from .base import BirdBase

provides = [Implementation(BirdBase)]
