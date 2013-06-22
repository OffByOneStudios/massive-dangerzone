"""plugin.py
@OffbyOne Studios 2013
Interface Object for Interfaces
"""
class Plugin(object):
    def __init__(self, **kwargs):
        self._args = kwargs

        def init_get(key, default=None):
            return self._args.get(key, default)

        self.name = init_get("name")
        self.version = init_get("version")
        self.implementation_name = init_get("implementation_name")

        self.language = init_get("language")

        self.imports = init_get("imports",[])
        self.depends = init_get("depends",[])

        self.declarations = init_get("declarations",{})
        self.variables = init_get("variables",{})


class Variable(object):
    """Data Structure for Variable Declarations.

    A Variable declaration is any declaration which requests space in memory.
        This is in contrast to Type Declarations, which define what kinds of things can request space in memory.
    """
    pass


class PluginDescription(object):
    """Data Structure for Declarations and Variables."""

    def __init__(self, declarations, variables, depends):
        """Constructor for PluginDescription helper class.

        Args:
            declarations: Dict of type definitions, whose keys are stringnames and whose values are types.
            variables: Dict of Variable declarations, whose keys are stringnames and whose values are either:
                1) keys into the declarations dict or B
                2) Anonymous types
            dependencies: Dict which maps namespaces to other plugin description objects.
        """
        self.declarations = declarations
        self.variables = variables
        self.depends = depends


    @staticmethod
    def split_namespace(stringname):
        """Splits stringname into namespace,symbol pair
        args:
            stringname: fully qualified name of symbol

        returns: (namespace, syombol) string pair.

        """
        split_name = stringname.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])
        return (namespace, end_name)

    def get_type(self, stringname):
        """Getter for type declarations.

        Args:
            stringname: string containing name of declaration.
        """
        namespace,symbol = self.split_namespace(stringname)
        if namespace == "":
            return self.declarations[stringname]
        else:
            # TODO Exception Checking
            return self.dependencies[namespace].description.get_type(symbol)

