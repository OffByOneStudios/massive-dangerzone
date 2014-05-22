from .exceptions import *
from .EntityFacade import EntityFacade

def syntax_for(system):
    import inspect
    import pyext
    
    from .. import abstract as abstract
    
    system.current = system
    
    if not isinstance(system, abstract.ISystem):
        raise Exception("System argument '{}' is not an instance of ISystem.".format(system))

    def get_current_system(cls, __system=system):
        return __system.current

    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])

    syntax_vars = map(lambda c: (c[0], type(c[0], (c[1], ), {
            "_get_current_system": classmethod(get_current_system)
        })), [
            ("Entity", EntityFacade)
        ])

    for attr, value in syntax_vars:
        value.__module__ = module.__name__
        setattr(module, attr, value)

class ManagerKey(str): pass

def manager_for(system):
    from .. import abstract as abstract

    system = system.current

    def dec(cls, _system=system):
        if not issubclass(cls, abstract.IComponentManager):
            raise Exception("Decorated class '{}' is not a subclass of IComponentManager.".format(cls))

        _system.add_manager(cls, cls())

        return cls
    return dec

def index_for(system, manager_key):
    from .. import abstract as abstract

    system = system.current
    manager = system.get_manager(manager_key)

    def dec(cls, _system=system, _manager=manager):
        if not issubclass(cls, abstract.IComponentIndex):
            raise Exception("Decorated class '{}' is not a subclass of IComponentIndex.".format(cls))

        index = cls(_manager)
        _system.add_index(cls, index)
        
        return cls
    return dec
