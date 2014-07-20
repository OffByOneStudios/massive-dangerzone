"""pydynecs/serialization/PyObjFakeSerializer.py
@OffbyOne Studios 2014
Fake standin serializer for pyobj (picklable) components.
"""

from .. import abstract

class PyObjFakeSerializer():
    def __init__(self, system):
        pass
    
    def pack(self, key, component):
        return component
    
    def unpack(self, key, packed):
        return packed