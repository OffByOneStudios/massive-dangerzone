import logging
import os
import sys
import imp
import traceback

from . import system_config as sys_cfg
from . import languages

logger = logging.getLogger(__name__)

class ConfigLoader(object):
    def __init__(self, root):
        self._root = root
        self._loaded_langs = {}

    def _load_language(self, name):
        if name in self._loaded_langs:
            return self._loaded_langs[name]
        try:
            self._loaded_langs[name] = languages.get_language(name).config
            return self._loaded_langs[name]
        except:
            return None

    def _parse_language_config(self, lang_option, value):
        lang_cfg = self._load_language(lang_option.get_language_name())
        parsed_options = []

        for (key, value) in self.value.items():
            if hasattr(lang_cfg, key):
                option = getattr(lang_cfg, key)
                try:
                    parsed_options.append(option(value))
                except:
                    logger.info("Failed to construct option '{}' (with value '{}'). Skipping!".format(option, value))

        return lang_option(lang_cfg.Config(parsed_options))

    def parse_system_config(self):
        parsed_options = []
        for (key, value) in self._root.items():
            if hasattr(sys_cfg, key):
                option = getattr(sys_cfg, key)
                # Branch based on special parse types here
                if isinstance(option, sys_cfg.BaseLanguageDefaultConfig):
                    try:
                        parsed_options.append(self._parse_language_config(option, value))
                    except:
                        logger.info("Failed to parse language config option '{}' (with value '{}'). Skipping!".format(option, value))
                # Default parse type
                else:
                    try:
                        parsed_options.append(option(value))
                    except:
                        logger.info("Failed to construct option '{}' (with value '{}'). Skipping!".format(option, value))
            else:
                logger.info("Failed to parse option '{}' (with value '{}'). Skipping!".format(key, value))

        return sys_cfg.SystemConfig(parsed_options)

def load_config_from_file(filename, varname="config"):
    with open(filename) as module_file: #TODO(Mason): Figure out this name
        try:
            module = imp.load_module("a_config", module_file, filename, ('.py', 'r', imp.PY_SOURCE))
            config = getattr(module, varname)
            loader = ConfigLoader(config)
            return loader.parse_system_config()
        except:
            tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
            logger.info("Failed to load config from file '{}':\n\t{}".format(filename, tb_string))
            return None

