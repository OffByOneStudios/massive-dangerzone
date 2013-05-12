import nature

from nature.animal.bird import BirdBase as BirdBaseOld
BirdBaseNew = nature.__domain__.import("animal.bird", version="0.6.0")


