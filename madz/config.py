"""config.py
@OffbyOneStudios 2013
Code to provide helper types in the configuration of the system.
"""

class BaseOption(object):
    default_value=None

    @classmethod
    def get_default_value(cls):
        return cls.default_value

    def __init__(self, value=None):
        self.value = value if not (value is None) else self.get_default_value()

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


class BaseAppendOption(BaseOption):
    default_value=[]

    def overwrite(self, other_option):
        self.value.extend(other_option.value)


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

    def get_option(self, type, default=None):
        return self._opt_dict.get(type.get_key(), None)

    def get(self, type, default=None):
        key=type.get_key()
        if key in self._opt_dict:
            return self._opt_dict[key].value
        else:
            return default

    def __getitem__(self, key):
        return self._opt_dict[key.get_key()].value

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


def merge_options(**args):
    """A helper function for merging many options, many which may not exist."""
    # Filter None options, return None if there are no valid options
    actual_args = list(filter(None, args))
    if len(actual_args) == 0:
        return None

    # Generate a default to start overwrites from, and onto
    base = actual_args[0].make_default()
    for option in actual_args:
        base.overwrite(option)

    return base

def merge_configs(*args, base_config=None):
    """A helper function for merging many configs, many which may not exist."""
    # Filter None configs, return None if there are no valid configs
    actual_args = list(filter(None, args))
    if len(actual_args) == 0:
        return base_config

    # Generate a default to start extensions from, and onto
    base = actual_args[0].make_default() if (base_config is None) else base_config
    for config in actual_args:
        base.extend(config)

    return base

