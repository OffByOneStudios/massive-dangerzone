from ..core import *

from .exceptions import *

def system_syntax(system):
    import inspect
    import pyext
    
    from .. import abstract as abstract
    
    if not issubclass(system, abstract.ISystem):
        raise Exception("System argument '{}' is not a subclass of ISystem.".format(system))

    def get_current_system(cls, __system=system):
        return __system.current

    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])

    syntax_vars = list(map(lambda c: (c[0], type(c[0], (c[1], ), {
            "_get_current_system": classmethod(get_current_system)
        })), [
            ("Entity", EntityFacade)
        ]))

    for attr, value in syntax_vars:
        value.__module__ = module.__name__
        setattr(module, attr, value)
        
    for attr, value in syntax_vars:
        setattr(system, attr, value)
        
    return system

def manager_decorator_for(system):
    from .. import abstract as abstract

    def dec(cls, _system=system):
        if not issubclass(cls, abstract.IEntityManager):
            raise Exception("Decorated class '{}' is not a subclass of IEntityManager.".format(cls))
        
        cls.pydynecs_key = classmethod(lambda cls=cls: "{}/{}".format(cls.__module__, cls.__qualname__))
        cls.pydynecs_ecsclass = _system
        abstract.IManagerKey.register(cls)

        _system.add_manager(cls, cls)
        
        return cls
    return dec
