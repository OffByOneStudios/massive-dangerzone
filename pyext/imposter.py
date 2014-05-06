"""pyext/imposter.py
@OffbyOne Studios 2014
A library for creating imposter objects using a dictionary.
"""

class Imposter(object):
    def __init__(self, lookup):
        self.__lookup = lookup
    
    def __getattr__(self, name):
        return self.__lookup[name]
    
    def __setattr__(self, name, value):
        self.__lookup[name] = value
    
    def __delattr__(self, name):
        raise AttributeError(name)
        

class ImposterModule(Imposter):
    def __init__(self, lookup, name, base_module):
        super().__init__(lookup)
        self.__module__ = base_module + "." + name
