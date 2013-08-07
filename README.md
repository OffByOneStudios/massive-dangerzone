Massive Dangerzone
==================

Summary
------------------

Massive-Dangerzone, abreviated madz, is a plugin management system built on python. Plugins can be written in any supported programming language. Plugins communicate through their CFFI (C Foreign Function Interface), often wrapped by support source files to ease programmer usability. Wrapper files are generated from an intermediate description language, MDL (Madz Description Language).

Currently supported languages:
* C
* C++
* Python (v3)

Purpose
------------------

The purpose of madz is to provide a flexible and customizable framework for very large projects to build within. It is not meant for small projects, projects where a single language can provide the majority of features. It's not even meant meant for medium projects, where dual languages might suffice, one language providing the heavy lifting, and the other the scripting. 

Madz is designed for massive projects with large and diverse sets of requriments. Here are some cases madz will excel at:
* Allowing users to add custom features. Using languages and libraries of their choice. And then letting them glue it into the existing system using just their language and MDL. These plugins could even be compiled and loaded without access to the entire project.
* Allowing multiple versions and implementations of the same plugin to exist. Making rewrites easier, as they can both exist side by side, with developers being able to choose which one they want on the fly.
* Abstracting platform features behind plugins automatically. Plugins for other features will simply be ignored when run on those systems. Features can include operating systems, hardware and software installed, processor features, and anything else.
* Abstrcting interpreter and compiler choice. Language configuration is seperate from compiler choices and configuration. Specify custom compilers and interpreters and compare their performence, or choose a stock one.
* Organizing large projects. Organize a project however you see fit with many folder and documentation structures. Overlay your custom plugins on top of an exisiting plugin system by simply adding a directory to the load list by writing a simple custom start script to wrap the existing one.
* Unified command system for the entire project. One thing is responsible for all manipulation of the project, no need to worry about configuring multiple build systems, packaging systems, ect.

Future Improvements
------------------

Planned languages:
* ~~C~~ - A static imperative language, usefulf or systems programming.
* ~~C++~~ - A language with static class based objects, useful for organized fast code.
* ~~Python~~ - A dynamic imperative language, has monkey patchable objects, useful for general scripting.
* Scheme - A dynamic functional language, useful for runtime scripting via macros.
* Haskell - A static functional language, useful for algorithms (completes all four combinations of imperative/functional and static/dynamic).
* JVM/Java - A VM based language. (Although any java language would likely work well through their java compatability interface).

Other features:
* Development Modes
* Custom Commands
* Packaging
* Dynamic Plugin Loading
* Self Implementation (Implementing Madz as a Madz plugin system.)
* Standard Library
* MDL Extensions (Datatypes, Objects)
* Static Compilation

Wishlist languages (not in our schedule, but would like to see added; kind of sorted in order of difficulty):
* Lua - A common embedded scripting language.
* Go/Rust - A neo-systems programming language.
* Common Lisp - A production "real world" style lisp.
* Javascript - Web assembly.
* Smalltalk - A message passing object oriented language.
* CLR/C# - Microsoft's JVM alternative.

Wishlist features (not in our schedule, but would like to see added):
* Documentation Generation (MDL, and then, cross language).
* MDL Extensions (Aspects, Thread attributes, Const attributes, ect.)
* Optimization using the above attributes.
* Multiplugin, single source code. (Project a single set of source code into many resulting plugins, for exmaple, compiling with different platform flags, and packging all of them.)
* Piecemeal package and download system. (Solving the same problem as the above, compile/choose plugins for a package on the fly as needed.)

Features
==================

__Madz is still in development, features described below (and above) are subject to change, may not be finished, or may never exist (that goes extra for undocumented features that may currently be working)__

Plugin Directories
------------------
Plugins are stored in directories. A plugin system, can have multiple directories. Most plugin metadata related to resolution may be stored in it's path.


    the.namespace.of.plugin[1.0.2-alpha+42](an_implementation_name)


The above is a folder name for a plugin with the following metadata:


    name                = "the.namespace.of.plugin"
    version             = "1.0.2-alpha+42"
    implementation_name = "an_implementation_name"


The following are equivelent folder layouts (where '/' represents a folder seperator):


    the/namespace.of/plugin/[1.0.2-alpha+42]/(an_implementation_name)
    the.namespace.of.plugin/[1.0.2-alpha+42](an_implementation_name)

Metadata in folder paths must always match the metadata given in plugin stubs.


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
Madz has 3 layers of user configuration, applied in the following order (i.e. the later ones overwrite the previous ones):

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


Plugin Resolution
------------------

TODO: Describe this.


MDL
------------------
The __M__adz __D__escription __L__anguage. For the time being this is used as a raw abstract syntax tree definied using python objects.

TODO: Finish describing this.


Madz Library
------------------

TODO: Describe this.


Madz Runtime
------------------

TODO: Describe this.


MIP
------------------
The __M__adz __I__nter-plugin __P__rotocol. This is the protocol observed by madz plugins. If a dynamic object follows this protocol it can be used as a madz plugin. This description is meant more for language wrapper implementors, working within the existing Madz infrastructure.

TODO: Finish describing this.


