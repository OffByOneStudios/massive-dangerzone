"""pyext/imposter.py
@OffbyOne Studios 2014
A library for creating imposter objects (and modules) using a dictionary.
"""

class Imposter(object):
    """An imposter object using a dictionary for attr lookups.

    All functions raise key errors on failue (as opposed to attribute errors.)
    """
    def __init__(self, lookup):
        self.__lookup = lookup

    def __getattr__(self, name):
        return self.__lookup[name]

    def __setattr__(self, name, value):
        self.__lookup[name] = value

    def __delattr__(self, name):
        del self.__lookup[name]


class ImposterModule(Imposter):
    """An imposter module for dynamic python namespace creation."""
    def __init__(self, lookup, name, base_module):
        """Initializes an imposter module using a dictionary and module information.

        Args:
            lookup: The dictionary like object to use for attributes.
            name: The final name of the object.
            base_module: The module name of the parent module.
        """
        super().__init__(lookup)
        self.__module__ = base_module + "." + name
