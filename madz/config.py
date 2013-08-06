"""config.py
@OffbyOneStudios 2013
Code to provide helper types in the configuration of the system.
"""

class BaseOption(object):

    @classmethod
    def get_key(cls):
        return cls

    @classmethod
    def make_default(cls):
        return cls()

    def get_value(self):
        return self.value

    def overwrite(self, other_option):
        self.value = other_option.value

class BaseConfig(object):
    def __init__(self, options=None):
        if options == None:
            options = self._default_options()
        self._opt_dict = dict([(option.get_key(), option) for option in options])

    def _default_options(self):
        return []

    @classmethod
    def get_key(cls):
        return cls

    @classmethod
    def make_default(cls):
        return cls()

    def get_option(self, type):
        return self._opt_dict[type.get_key()]

    def __getitem__(self, key):
        return self.get_option(key).value

    def add_option(self, option):
        if option.get_key() in self._opt_dict:
            self._opt_dict[option.get_key()].overwrite(option)
        else:
            self._opt_dict[option.get_key()] = option

    def all_options(self):
        return self._opt_dict.values()

    def extend(self, other_config):
        for opt in other_config.all_options():
            self.add_option(opt)


