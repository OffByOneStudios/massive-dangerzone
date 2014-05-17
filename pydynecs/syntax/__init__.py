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

def syntax_manager(system, key, manager):
    import inspect

    from .. import abstract as abstract

    system = system.current

    if not isinstance(manager, abstract.IComponentManager):
        raise Exception("Manager argument '{}' is not an instance of IComponentManager.".format(manager))

    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])
    
    full_key = ManagerKey("{}/{}".format(module.__name__, key))

    system.add_manager(full_key, manager)

    setattr(module, key, full_key)

def syntax_index(system, manager_key, key, index):
    from .. import abstract as abstract

    system = system.current

    if not isinstance(index, abstract.IComponentIndex):
        raise Exception("Index argument '{}' is not an instance of IComponentIndex.".format(manager))

    index_key = ManagerKey("{}#{}".format(manager_key, key))
    
    manager = system.get_manager(manager_key)
    index.attach(manager)
    system.add_index(index_key, index)
    
    setattr(manager_key, key, index_key)
