"""action/execute.py
@OffbyOne Studios 2013
Action for executing a plugin.
"""
from ctypes import *

import logging

from .. import operating_system
from ..MDL.py_ctypes_gen import set_ctypes_from_mdl

from ..config import *
from madz.daemon.minion.executer import *

from .base import *

logger = logging.getLogger(__name__)

class ExecuteAction(BaseAction):
    """Executes a function from a plugin."""
    action_name = "execute"

    def __init__(self, system):
        BaseAction.__init__(self, system)
        self._operating = operating_system.get_system()

    def do(self):
        """Executes a plugin on the associated system."""
        execute_plugin_name = config.get(OptionSystemExecutePlugin)
        execute_function_name = config.get(OptionSystemExecuteFunctionName)

        logger.debug("Loading plugins for '{}' targeting function '{}'.".format(
                execute_plugin_name,
                execute_function_name
            ))

        if execute_plugin_name is None:
            logger.error("ACTION[{}] cannot execute. OptionSystemExecutePlugin is not defined.".format(self.action_name))
            return

        try:
            plugin_stub = self.system.resolve_plugin(execute_plugin_name)
            exec_minion = Daemon.current.spawn_minion(ExecuterMinion)[0]    
            exec_minion.execute()

            exec_minion.load(plugin_stub)

            logger.info("ACTION[{}] Calling function '{}' from plugin '{}'.".format(self.action_name, execute_function_name, execute_plugin_name))
            exec_minion.call_func(plugin_stub, execute_function_name)

            logger.info("ACTION[{}] Completed, new instance started!".format(self.action_name))
        except Exception as e:
            tb_string = "\n\t".join(("".join(traceback.format_exception(*sys.exc_info()))).split("\n"))
            logger.error("ACTION[{}] failed on plugin '{}':\n\t{}".format(self.action_name, plugin_stub, tb_string))

