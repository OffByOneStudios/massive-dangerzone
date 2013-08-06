from . import config

class SystemConfig(config.BaseConfig):
    """Configuration for the whole system.

    """
    def _default_options(self):
        return [
            OptionSkipDependencies(),
        ]

class OptionSkipDependencies(config.BaseOption):
    """This option determines if the system uses dependencies or not to prune what to build."""
    def __init__(self, value=False):
        self.value = value

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

