Massive Dangerzone
==================

Summary
------------------

Massive-Dangerzone, abreviated madz, is a plugin management system built on python. Plugins can be written in any supported programming language. Plugins communicate through their CFFI (C Foreign Function Interface), often wrapped by support source files to ease programmer usability. Wrapper files are generated from an intermediate description language, MDL (Madz Description Language).

Currently supported languages:
* C
* C++
* Python3

Future Improvements
------------------

Planed languages:
* Scheme
* Haskell
* JVM/Java (Although any java language would likely work well through their java compatability interface).

Other features:
* Development Modes
* Custom Commands
* Packaging
* Dynamic Plugin Loading
* Self Implementation (Implementing Madz as a Madz plugin system.)
* Standard Library
* MDL Extensions (Datatypes, Objects)
* Static Compilation

Features
==================

__Madz is still in development, features described below are likely subject to change, may not be finished, or may never exist (that goes extra for undocumented features currently working)__

Plugin Directories
------------------
Plugins are stored in directories. Most plugin metadata related to resolution may be stored in it's path.


    the.namespace.of.plugin[1.0.2-alpha+42](an implementation name)


The above is a folder name for a plugin with the following metadata:


    name                = "c.set0"
    version             = "0.1.0"
    implementation_name = "an_implementation_name"


The following are equivelent folder layouts (where '/' represents a folder seperator):


    the/namespace.of/plugin/[1.0.2-alpha+42]/(an_implementation_name)
    the.namespace.of.plugin/[1.0.2-alpha+42](an_implementation_name)


Plugin Stubs
------------------
Plugin stubs are the representation of all metadata relating to a plugin. For the time being they are represented by `__plugin__.py` files in the plugin folder. They use python as a scripting language to allow arbitrary information for the time being.

TODO: List properties. Give examples.


Language Compatability Wrappers
------------------
See the wiki for each language implementation:

* C - "c"
* C++ - "cpp"
* Python - "python"

TODO: Write information on these.


Configuration
------------------
Madz has 3 layers of configuration, applied in the following order (i.e. the later ones overwrite the previous ones):

* __Default__ - The default configurations. A psuedo layer since users can't really change it.
* __User__ - A per machine configuration primarily for providing locations on the system for libraries, headers, compilers, ect. Set via environment variable.
* __System__ - A per system (of plugins) configuration for providing commands, modes, custom rules for the system, ect. Set via the startup script.
* __Plugin__ - A per plugin configuration for providing plugin specific library imports, optimizations, and build rules. Set via the plugin stub.

Configurations are also full python files, allowing for, theoretically, arbitrary power. Default implementations (will in the future) include the following features:

* User defined compilers.
* Compiling librarires and headers.
* Specifying paths to find the above.
* Architecture specific configuration resolution. (Choose A on platform X, Choose B on platform Y [On can be replaced with "for target"])
* User defined modes (e.g. "debug", "release", "safe", "metric" (many of these may have drop in default versions availble))
* User defined commands (e.g. "build", "clean", "wrap", "check", "package", "run" (many of these may have drop in default versions availble))

TODO: Link the above to wiki.

