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
    ## System options
    OptionSystemSkipDependencies(),
    OptionSystemExecuteFunctionName(),
    OptionSystemExecuteFunctionSignature(),

    ## Compiler defaults
    OptionImposter(lambda: {
        "windows": OptionCompilerPreference("cl"),
        "unix": OptionCompilerPreference("gcc"),
        "osx": OptionCompilerPreference("clang")
        }[config_source.get(OptionPlatformOperatingSystem)]),

    ## Commands
    # Main commands
    command.CommandConfig("all", [
        command.OptionCommandActions(["clean", "wrap", "build", "load", "execute"]),
    ]),
    command.CommandConfig("main", [
        command.OptionCommandActions(["wrap", "build", "load", "execute"]),
    ]),

    # Piecemeal commands
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
    command.CommandConfig("remake", [
        command.OptionCommandActions(["clean", "wrap", "build"]),
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