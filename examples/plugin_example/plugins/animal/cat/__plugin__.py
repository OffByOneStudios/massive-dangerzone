from magic.plugins import *

name = "animal.cat"
version = "0.0.1"

requires = [Interface("kingdom.animal.IAnimal")]

from .base import CatBase

provides = [Implementation(CatBase, of="kingdom.animal.IAnimal")]
