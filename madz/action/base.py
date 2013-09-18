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
    """Manages core action facilities.
    
    Attributes:
        system: The system for which actions are being applied.
    """
    action_name = "<BASE>"

    def __init__(self, system):
        self.system = system

    def do(self, plugins=None):
        """Applies the actions associated with the plugins within the Action's system."""
        #TODO(Mason): Make the plugins variable do something.
        active_plugins = self.system.active_plugins()

        logger.info("ACTION[{}] performing across {} plugins.".format(self.action_name, len(active_plugins)))

        for plugin in active_plugins:
            self.do_plugin(plugin)

    def _check_dependency(self, action_provider):
        return config.get(OptionSystemSkipDependencies) or not (action_provider.get_dependency())

    def _get_provider(self, language):
        #TODO(Mason): Implement this function.
        raise NotImplementedError()

    def do_plugin(self, plugin_stub):
        """Given a plugin, preforms the actions associated with the plugin on the current system."""
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
