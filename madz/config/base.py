"""config/base.py
@OffbyOneStudios 2013
Provides the base portions of the config system.

BaseOption: is the base option type from which all inherit.
BaseAppendOption: is a helper option for any options which merge with list concatenation.
BaseConfigOption: is a helper option for options which contain other configs.

BaseConfig: is the base config type from which all inherit.
"""

import abc

class ConfigError(Exception): pass

#
# Options
#

class BaseOptionError(ConfigError): pass

class OptionInvalidValueError(BaseOptionError): pass
class OptionMergeError(BaseOptionError): pass
class OptionCoerceError(BaseOptionError): pass

class BaseOption(object):
    """The base option object. Always derive options from this object.

    Useful override functions:
        @classmethod get_key: The key the option goes by in configs. For options to be merged by configs this must match.
        @classmethod _validate_value: Checks to see if a value is valid before it is set. Checked during contruction and after merges. Except is false. Defaults to return True.
        @classmethod _coerce_value: Attemps to coerce the value to the correct type before validating. May throw exceptions.
        _merge_test: Checks to see if two options are mergeable, false will result in an exception. Uses get_key by default.
        _compute_merge_value: Calculates the merge of self and another option. Result must pass _validate_value.
    """
    __metaclass__ = abc.ABCMeta

    default_value=None

    @classmethod
    def get_default_value(cls):
        return cls.default_value

    def __init__(self, value=None):
        value = (value if not (value is None) else self.get_default_value())
        value = self._try_coerce_value(value)
        if not self._validate_value(value):
            raise InvalidValueError("Value '{}' is not valid, cannot __init__.".format(value))
        self._value = value

    @classmethod
    def get_key(cls):
        return cls

    @classmethod
    def make_default(cls):
        return cls()

    @classmethod
    def make(cls, value):
        return cls(value)

    def copy(self):
        return self.make(self.get_value())

    def get_value(self):
        return self._value

    @classmethod
    def _validate_value(cls, value):
        return True

    @classmethod
    def _coerce_value(cls, value):
        return value

    @classmethod
    def _try_coerce_value(cls, value):
        try:
            return cls._coerce_value(value)
        except Exception as exc:
            raise OptionCoerceError("Failed to coerce value.") from exc

    def _merge_test(self, other_option):
        return self.get_key() != other_option.get_key()

    def _merge_check(self, other_option):
        if self._merge_test(other_option):
            raise OptionMergeError(
                "Option keys (self='{}', other='{}') do not match, cannot merge.".format(
                    self.get_key(),
                    other.get_key()))

    def _compute_merge_value(self, other_option):
        return other_option.get_value()

    def _get_merge_value(self, other_option):
        new_value = self._compute_merge_value(other_option)

        new_value = self._try_coerce_value(new_value)

        if not self._validate_value(new_value):
            raise InvalidValueError("Value '{}' is not valid, cannot __init__.".format(value))

        return new_value

    def merge(self, other_option):
        self._merge_check(other_option)
        return self.make(self._get_merge_value(other_option))

    def apply(self, other_option):
        self._merge_check(other_option)
        self.value = self._get_merge_value(other_option)

    def _str_key(self):
        key = self.get_key()
        if (type(key) is tuple) and key[0] is self.__class__:
            return tuple(key[0].__name__, *(key[1:]))
        elif key is self.__class__:
            return key.__name__
        return key

    def __str__(self):
        return "{!s}: {!s}".format(self._str_key(), self.get_value())


class BaseAppendOption(BaseOption):
    default_value=[]

    @classmethod
    def _coerce_value(cls, value):
        return list(value)

    def _compute_merge_value(self, other_option):
        return self.get_value() + other_option.get_value()


class BaseBoolOption(BaseOption):

    @classmethod
    def _coerce_value(cls, value):
        return bool(value)


class BaseChooseOption(BaseOption):
    possible_values=[]

    @classmethod
    def _validate_value(cls, value):
        return (value in cls.possible_values)


class BaseSetOption(BaseOption):
    default_value=[]

    @classmethod
    def _coerce_value(cls, value):
        return list(value)

    def _compute_merge_value(self, other_option):
        #TODO set union/subtractions
        pass


#
# Configs
#

class BaseConfigError(ConfigError): pass

class ConfigMergeError(BaseConfigError): pass

class BaseConfig(object):
    __metaclass__ = abc.ABCMeta

    default_options=[]

    def __init__(self, options=[]):
        self._opt_dict = dict()

        options = self.get_default_options() + options
        for opt in options:
            self.apply_option(opt)

    @classmethod
    def get_default_options(cls):
        return cls.default_options

    def get_key(self):
        return self.__class__

    def get_value(self):
        return self

    @classmethod
    def make_default(cls):
        return cls()

    @classmethod
    def make(cls, value):
        return cls(value)

    def copy(self):
        return self.make(map(lambda o: o.copy(), self.get_options()))

    def get_option(self, key, default=None):
        """Gets the option object sharing a key with the given type parameter, may return a default option."""
        return self._opt_dict.get(key, None)

    def get(self, key, default=None):
        """Gets the value stored in the option object sharing a key with the given type parameter, may return a default value."""
        if key in self._opt_dict:
            return self._opt_dict[key].get_value()
        else:
            return default

    def __getitem__(self, key):
        """Gets the value, may cause exceptions."""
        return self._opt_dict[key].get_value()

    def get_options(self):
        return self._opt_dict.values()

    def apply_option(self, option):
        if option.get_key() in self._opt_dict:
            self._opt_dict[option.get_key()] = self._opt_dict[option.get_key()].merge(option)
        else:
            self._opt_dict[option.get_key()] = option

    def _merge_test(self, other_option):
        return self.get_key() != other_option.get_key()

    def _merge_check(self, other_option):
        if self._merge_test(other_option):
            raise ConfigMergeError(
                "Config keys (self='{}', other='{}') do not match, cannot merge.".format(
                    self.get_key(),
                    other.get_key()))

    def apply(self, other_config):
        self._merge_check(other_option)
        for opt in other_config.all_options():
            self.apply_option(opt)

    def merge(self, other_config):
        self._merge_check(other_option)
        new_config = self.copy()
        new_config.apply(other_config)
        return new_config

    def _str_view(self):
        return str(self.__class__)

    def __str__(self):
        return "{}:\n\t{}".format(
            self._str_view(),
            "\n\t".join(map(
                lambda o: "\n\t".join(str(o).split("\n")),
                self.get_options())))


#
# Helpers
#

def GenerateOption(basetype, name, default_value):
    """A helper function to generate options."""
    #TODO
    raise NotImplementedError

def merge(*args):
    """A helper function for merging many configs, many which may not exist."""
    # Filter None configs, return None if there are no valid configs
    actual_args = list(filter(None, args))
    if len(actual_args) == 0:
        return None

    # Generate a default to start extensions from, and onto
    base = actual_args[0]
    for config in actual_args[1:]:
        base = base.merge(config)

    return base


class OptionImposter(BaseOption):
    """This is a helper which allows a function to provide the option at config lookup time."""
    __metaclass__ = abc.ABCMeta

    default_value=None

    def get_default_value(cls):
        return cls.default_value

    def __init__(self, gen_func):
        self._gen_func = gen_func

    def get_key(self):
        return self._gen_func().get_key()

    def make_default(cls):
        return self._gen_func().__class__()

    def make(cls, value):
        return self._gen_func().__class__(value)

    def copy(self):
        return self.make(self._gen_func)

    def get_value(self):
        return self._gen_func().get_value()

    def merge(self, other_option):
        self._merge_check(other_option)
        return self.make(self._gen_func()._get_merge_value(other_option))

    def apply(self, other_option):
        pass

    def __str__(self):
        return "<IMPOSTER> {!s}: {!s}".format(self.get_key(), self.get_value())


