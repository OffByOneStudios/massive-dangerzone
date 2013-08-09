from . import config

class SystemConfig(config.BaseConfig):
    """Configuration for the whole system.

    """
    def _default_options(self):
        return [
            OptionSkipDependencies(),
        ]

    def get_default_language_config(self, language_name):
        res = list(filter(
            lambda opt: 
                isinstance(opt, BaseLanguageDefaultConfig) and 
                opt.get_language_name() == language_name,
            self._opt_dict))
        if len(res) > 1:
            #TODO, specific exception
            raise ValueError
        return res[0] if len(res) != 0 else None

class OptionSkipDependencies(config.BaseOption):
    """This option determines if the system uses dependencies or not to prune what to build."""
    default_value = False

class BaseLanguageDefaultConfig(config.BaseOption):
    @classmethod
    def get_language_name(self):
        return None

    def overwrite(self, other_option):
        self.value.extend(other_option.value)

class LanguageCDefaultConfig(BaseLanguageDefaultConfig):
    @classmethod
    def get_language_name(self):
        return "c"

class LanguageCPPDefaultConfig(BaseLanguageDefaultConfig):
    @classmethod
    def get_language_name(self):
        return "cpp"

class LanguagePythonDefaultConfig(BaseLanguageDefaultConfig):
    @classmethod
    def get_language_name(self):
        return "python"

