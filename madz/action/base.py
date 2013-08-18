"""action/base.py
@OffbyOne Studios 2013
Base action library. Ensures config loading.
"""
import sys
import logging
import traceback

from ..config import *

logger = logging.getLogger(__name__)

class BaseAction(object):
    """Manages core action facilities."""
    action_name = "<BASE>"

    def __init__(self, system):
        self.system = system

    def do(self):
        for plugin in self.system.active_plugins():
            self.do_plugin(plugin)

    def _check_dependency(self, action_provider):
        return config.get(OptionSystemSkipDependencies) or not (action_provider.get_dependency())

    def _get_provider(self, language):
        raise NotImplementedError()

    def do_plugin(self, plugin_stub):
        with plugin_stub.and_configs():
            language = plugin_stub.language
            provider = self._get_provider(language)
            
            if self._check_dependency(provider):
                logger.info("ACTION[{}] on plugin '{}'".format(self.action_name, plugin_stub))
                try:
                    provider.do()
                except Exception as e:
                    tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
                    logger.error("ACTION[{}] failed on plugin '{}':\n\t{}".format(self.action_name, plugin_stub, tb_string))
