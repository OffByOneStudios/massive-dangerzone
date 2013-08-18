"""config/__init__.py
@OffbyOne Studios 2013
Forwards config library and options.
"""
from .base import *
from .current import *

from .platform import *

from .user import *
from .system import *
from .plugin import *

from .command import *
from .mode import *
from .library import *
from .language import *
from .compiler import *

class DefaultConfig(BaseConfig):
	pass

DefaultConfig.default_options = [
		OptionSystemSkipDependencies(),
        command.CommandConfig("all", [
            command.OptionCommandActions(["wrap", "build", "load", "execute", "clean"]),
        ]),
        command.CommandConfig("main", [
            command.OptionCommandActions(["wrap", "build", "load", "execute"]),
        ]),

        command.CommandConfig("init", [
            command.OptionCommandActions([]),
        ]),
        command.CommandConfig("wrap", [
            command.OptionCommandActions(["wrap"]),
        ]),
        command.CommandConfig("build", [
            command.OptionCommandActions(["build"]),
        ]),
        command.CommandConfig("make", [
            command.OptionCommandActions(["wrap", "build"]),
        ]),
        command.CommandConfig("load", [
            command.OptionCommandActions(["load"]),
        ]),
        command.CommandConfig("execute", [
            command.OptionCommandActions(["load", "execute"]),
        ]),
        command.CommandConfig("clean", [
            command.OptionCommandActions(["clean"]),
        ]),
    ]

config.add(DefaultConfig())