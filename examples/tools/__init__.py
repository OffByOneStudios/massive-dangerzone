import os
import madz
import madz.bootstrap

from . import core

#madz.bootstrap.import_plugins_from_folders(os.path.dirname(__file__), exclude=["core"])

def start(target=None):
    if target is None:
        target = core.ToolChooser.identity()
    core.launch(madz.bootstrap.EcsBootstrap.current[core.Tool_identity][target])