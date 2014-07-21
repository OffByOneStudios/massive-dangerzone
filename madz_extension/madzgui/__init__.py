import os
import madz
import madz.bootstrap

from . import core
import madzgui.tools

def start(target=None):
    core.connect_replicated_ecs()
    if target is None:
        from madzgui.tools.ToolChooser import ToolChooser
        target = ToolChooser.identity()
    core.launch(madz.bootstrap.EcsBootstrap.current[core.Tool_identity][target])