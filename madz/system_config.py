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


