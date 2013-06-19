"""interface.py
@OffbyOne Studios 2013
Interface Object for Interfaces
"""
class Plugin(object):
    def __init__(self, name, version,
                 requires, declarations):
        self.name = name
        self.version = version
        self.requires = requires
        self.declarations = declarations
      
