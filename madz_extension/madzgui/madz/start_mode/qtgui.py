"""madzgui:madz/start_mode/qtgui.py
@OffbyOne Studios 2014
Srtartmode for launching a qt based gui.
"""

from madz.bootstrap import *
import madz.start_mode.core as core

import madzgui

@bootstrap_plugin("madz.start_mode.qtgui")
class GUIStartMode(core.IStartMode):
    def startmode_start(self, argv, system, user_config):
        madzgui.start()
    
    @classmethod
    def startmode_identity(self):
        return "qtgui"