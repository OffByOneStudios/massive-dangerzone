"""madzmodule:module/new/NewModuleOperation.py
@OffbyOne Studios 2014
Module Operation which generates new modules.
"""

import time
import os
import logging

from madz.bootstrap import *
import madz.module as module

from madzmodule.module.core import *
from madzmodule.language.core import *

logger = logging.getLogger(__name__)

@bootstrap_plugin("madzmodule.module.new")
class NewModuleOperation(metaclass=abc.ABCMeta):
    """Class which generates new modules."""

    def moduleoperation_perform(self, **kwargs):
        """Perform this module operation."""

        plugins = list(map(module.EcsModules.current, module.EcsModules.current[module.Old].entities()))
        namespaces = [plugin.id.namespace for plugin in plugins]

        failure = False
        if not kwargs["force"] and kwargs["namespace"] in namespaces:
            logger.error("Namespace:{} Already Exists (try --force).".format(kwargs["namespace"]))
            failure = True

        for depend in kwargs["depends"]:
            if not kwargs["force"] and not depend in namespaces:
                logger.error("Dependent namespace:{} does not exists (try --force)".format(depend))
                failure = True

        for _import in kwargs["imports"]:
            if not kwargs["force"] and not depend in namespaces:
                logger.error("Import namespace:{} does not exists (try --force)")
                failure = True

        if failure:
            logger.error("Unable to resolve conflicts; abandoning new plugin")
            return

        kwargs["depends"] = ",\n    ".join(['"{}"'.format(i) for i in kwargs["depends"]])
        kwargs["imports"] = ",\n    ".join(['"{}"'.format(i) for i in kwargs["imports"]])
        kwargs["date"] = time.ctime()

        lang = get_newlanguage(kwargs["language"])()

        dir_path = os.path.join(
                kwargs["path"],
                kwargs["namespace"].replace(".", "/"),
                "({})".format(kwargs["name"]),
                "[{}]".format(kwargs["version"]))

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(os.path.join(dir_path, "__plugin__.py"), "w") as f:
            f.write(plugin_template.format(**kwargs))

        with open(os.path.join(dir_path, kwargs["mdl-name"]), "w") as f:
            f.write(mdl_template.format(**kwargs))

        with open(os.path.join(dir_path, "{}.md".format(kwargs["namespace"].split(".")[-1])), "w") as f:
            f.write(md_template.format(**kwargs))

        with open(os.path.join(dir_path, "madz.{}".format(lang.newlanguage_extension())), "w") as f:
            f.write(lang.newlanguage_generate(**kwargs))



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


mdl_template = \
"""#{mdl-name}
#@{author} {date}
#A New Module
"""

md_template = \
"""#{namespace}
#@{author} {date}
A New Module
"""
