from .exceptions import *
from .EntityFacade import EntityFacade

def inject_syntax_for(name, system):
    import sys
    import pyext
    from .. import abstract as abstract
    if not issubclass(system, abstract.ISystem):
        raise Exception("System argument '{}' is not an instance of ISystem.".format(system))

    def get_current_system(cls, __system=system):
        return __system.current

    module = sys.modules[name]

    syntax_vars = map(lambda c: (c[0], type(c[0], (c[1], ), {
            "_get_current_system": classmethod(get_current_system)
        })), [
            ("Entity", EntityFacade)
        ])

    for attr, value in syntax_vars:
        value.__module__ = module.__name__
        setattr(module, attr, value)
