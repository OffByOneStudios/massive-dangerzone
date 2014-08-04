"""madzmodule:module/new/CopyModuleOperation.py
@OffbyOne Studios 2014
Module Operation which generates new modules.
"""

import time
import os
import logging
import shutil

from madz.bootstrap import *
import madz.module as module

from madzmodule.module.core import *
from madzmodule.language.core import *

logger = logging.getLogger(__name__)

@bootstrap_plugin("madzmodule.module.copy")
class CopyModuleOperation(IModuleOperation):
    """Class which generates new modules."""

    def moduleoperation_perform(self, **kwargs):
        """Perform this module operation."""

        plugins = list(map(module.EcsModules.current, module.EcsModules.current[module.Old].entities()))
        namespaces = [plugin.id.namespace for plugin in plugins]

        failure = False

        if not kwargs["template"]in namespaces:
            logger.error("Template namespace:{} does not exist".format(kwargs["namespace"]))
            failure = True
        if not kwargs["force"] and kwargs["namespace"] in namespaces:
            logger.error("Namespace:{} Already Exists (try --force).".format(kwargs["namespace"]))
            failure = True

        if failure:
            logger.error("Unable to resolve conflicts; abandoning copy plugin")
            return


        template_plugin = None
        for p in plugins:
            if p.id.namespace == kwargs["template"]:
                template_plugin = p
                break

        kwargs["version"] = template_plugin.id.version or "0.1.0"
        kwargs["language"] = template_plugin.old.language
        kwargs["name"] = template_plugin.id.implementation
        kwargs["depends"] = ",\n    ".join(['"{}"'.format(i.id.namespace) for i in template_plugin.old.loaded_depends])
        kwargs["imports"] = ",\n    ".join(['"{}"'.format(i.id.namespace) for i in template_plugin.old.loaded_imports])

        dir_path = os.path.join(
            kwargs["path"],
            kwargs["namespace"].replace(".", "/"),
            "({})".format(kwargs["name"]),
            "[{}]".format(kwargs["version"]))

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for f in os.listdir(str(template_plugin.old.directory.path)):
            if os.path.splitext(f)[1] == ".mdl":
                kwargs["mdl-name"] = f
            if not os.path.isdir(os.path.join(str(template_plugin.old.directory.path), f)) and f != "__init__.py":
                shutil.copy(os.path.join(str(template_plugin.old.directory.path), f), os.path.join(dir_path, f))

        with open(os.path.join(dir_path, "__plugin__.py"), "w") as f:
            f.write(plugin_template.format(**kwargs))

    @classmethod
    def moduleoperation_identity(self):
        return "new"


plugin_template = \
"""from madz.plugin_stub import *

plugin = Plugin(
    name="{namespace}",
    implementation="{name}",
    language="{language}",
    version="{version}",

	depends=[
    {depends}
    ],

    imports=[
    {imports}
    ],

    documentation="A New Module",
    description=MdlFileLoader("{mdl-name}"),
)
"""
