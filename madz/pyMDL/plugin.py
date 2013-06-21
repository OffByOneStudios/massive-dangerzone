"""interface.py
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

        self.requires = init_get("requires")
        self.dependencies = init_get("dependencies")

        self.declarations = init_get("declarations")
