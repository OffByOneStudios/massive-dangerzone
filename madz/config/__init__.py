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

    OptionCompilerDebug(),
    OptionCompilerOptimization(),

    ## Modes
    ModeConfig("debug", [
        OptionCompilerDebug(True),
        OptionCompilerOptimization(0.0),
    ]),

    ## Commands
    # Main commands
    CommandConfig("all", [
        OptionCommandActions(["clean", "wrap", "build", "load", "execute"]),
    ]),
    CommandConfig("main", [
        OptionCommandActions(["wrap", "build", "load", "execute"]),
    ]),

    # Piecemeal commands
    CommandConfig("init", [
        OptionCommandActions([]),
    ]),
    CommandConfig("wrap", [
        OptionCommandActions(["wrap"]),
    ]),
    CommandConfig("build", [
        OptionCommandActions(["build"]),
    ]),
    CommandConfig("make", [
        OptionCommandActions(["wrap", "build"]),
    ]),
    CommandConfig("remake", [
        OptionCommandActions(["clean", "wrap", "build"]),
    ]),
    CommandConfig("load", [
        OptionCommandActions(["load"]),
    ]),
    CommandConfig("execute", [
        OptionCommandActions(["load", "execute"]),
    ]),
    CommandConfig("clean", [
        OptionCommandActions(["clean"]),
    ]),
]

config.add(DefaultConfig())