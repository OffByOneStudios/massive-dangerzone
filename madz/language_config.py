"""language_config.py
@OffbyOne Studios 2013
Manages the confiuration of plugin languages.
"""

from . import operating_systems

class LanguageConfig(object):
    def __init__(self, config, default_config):
        self.config = config
        self.default_config = default_config

    os = operating_systems.get_system_description()

    @classmethod
    def _get_config_list_from(cls, config_dict, key):
        ret = []

        nkey = "{}+{}".format(key, cls.os)
        if nkey in config_dict:
            ret.append(config_dict[nkey])

        if key in config_dict:
            ret.append(config_dict[key])

        return ret

    def get_config_list(self, key):
        return self._get_config_list_from(self.config, key) + \
            self._get_config_list_from(self.default_config, key)


