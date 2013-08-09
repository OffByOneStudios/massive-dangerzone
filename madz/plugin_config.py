from . import config

class PluginConfig(config.BaseConfig):
    """Configuration for a specific plugin.

    """
    def _default_options(self):
        return [
        ]

class OptionLanguageConfig(config.BaseOption):
    """Configuration for this plugins language specific language."""
    def overwrite(self, other_option):
        self.value.extend(other_option.value)
