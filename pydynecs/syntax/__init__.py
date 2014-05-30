from .exceptions import *
from .EntityFacade import EntityFacade

def system_syntax(system):
    import inspect
    import pyext
    
    from .. import abstract as abstract
    
    system.current = system()
    
    if not issubclass(system, abstract.ISystem):
        raise Exception("System argument '{}' is not a subclass of ISystem.".format(system))

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
    
    return system.current

def manager_decorator_for(system):
    from .. import abstract as abstract

    system = system.current

    def dec(cls, _system=system):
        if not issubclass(cls, abstract.IEntityManager):
            raise Exception("Decorated class '{}' is not a subclass of IEntityManager.".format(cls))
            
        cls.pydynecs_key = lambda cls=cls: "{}/{}".format(cls.__module__, cls.__qualname__)
        abstract.IManagerKey.register(cls)
        
        instance = cls()
        _system.add_manager(cls, instance)

        for name in dir(cls):
            if name.startswith("_"):
                continue
            actual = getattr(cls, name)
            if issubclass(actual, abstract.IEntityManager):
                if issubclass(actual, abstract.IIndexManager):
                    actual_instance = actual(instance)
                else:
                    actual_instance = actual()
                actual.pydynecs_key = lambda cls=actual: "{}/{}".format(cls.__module__, cls.__qualname__)
                abstract.IManagerKey.register(actual)
                _system.add_manager(actual, actual_instance)
        
        return cls
    return dec
