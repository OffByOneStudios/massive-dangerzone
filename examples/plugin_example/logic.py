import nature
import magic.interface

from nature.animal.bird import BirdBase as BirdBaseOld
BirdBaseNew = nature.__domain__.import("animal.bird", version="0.6.0")

def do_some_stuff()
    bird1 = BirdBaseOld()
    print bird1.sound() # "Kaww!"

    bird2 = BirdBaseNew()
    if isinstance(bird2, nature.kingdom.animal.IAnimal):
        raise Exception("Should not happen")
    print bird2.sound() # "Kaaw"

    cat = nature.animal.cat.CatBase()
    print cat.sound() # "Meow"
