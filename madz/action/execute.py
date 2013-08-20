"""action/execute.py
@OffbyOne Studios 2013
Action for executing a plugin.
"""
import logging

from .. import operating_system
from ..MDL.py_ctypes_gen import set_ctypes_from_mdl

from ..config import *

from .base import *

logger = logging.getLogger(__name__)

class ExecuteAction(BaseAction):
    """Executes a function from a plugin."""
    action_name = "execute"

    def __init__(self, system):
        BaseAction.__init__(self, system)
        self._operating = operating_system.get_system()

    def do(self):
        """Executes a plugin."""
        execute_plugin_name = config.get(OptionSystemExecutePlugin)
        execute_function_name = config.get(OptionSystemExecuteFunctionName)
        execute_function_signature = config.get(OptionSystemExecuteFunctionSignature)

        if execute_plugin_name is None:
            logger.error("ACTION[{}] cannot execute. OptionSystemExecutePlugin is not defined.".format(self.action_name))
            return

        try:
            plugin_stub = self.system.resolve(execute_plugin_name)
            function = self._get_function(plugin_stub, execute_function_name)
            function = set_ctypes_from_mdl(function, execute_function_signature)

            function()
        except Exception as e:
            tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
            logger.error("ACTION[{}] failed on plugin '{}':\n\t{}".format(self.action_name, plugin_stub, tb_string))

    def _get_function(self, plugin_stub, name):
        return self._operating.get_function(plugin_stub, name)
