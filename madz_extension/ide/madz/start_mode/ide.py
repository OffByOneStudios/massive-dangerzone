"""ide:madz/start_mode/ide.py
@OffbyOne Studios 2014
Startmode for launching ide helper functionality.
"""

from madz.bootstrap import *
import madz.start_mode.core as core

import ide

@bootstrap_plugin("madz.start_mode.ide")
class GUIStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        madzgui.start()
    
    @classmethod
    def startmode_identity(self):
        return "ide"