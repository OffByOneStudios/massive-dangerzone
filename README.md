Massive Dangerzone
==================

### Version: 0.3.0 ([CHANGES](https://github.com/OffByOneStudios/massive-dangerzone/blob/master/CHANGES.md))

Summary
------------------

Massive-Dangerzone, abbreviated madz, is a plugin management system built on python. Plugins can be written in any supported programming language. Plugins communicate through their CFFI (C Foreign Function Interface), often wrapped by support source files to ease programmer usability. Wrapper files are generated from an intermediate description language, MDL (Madz Description Language).

Currently supported languages:
* C
* C++
* Python (v3)

Purpose
------------------

The purpose of madz is to provide a flexible and customizable framework for very large projects to build within. It is not meant for small projects, projects where a single language can provide the majority of features. It's not even meant meant for medium projects, where dual languages might suffice, one language providing the heavy lifting, and the other the scripting. 

Madz is designed for massive projects with large and diverse sets of requirements. Here are some cases madz will excel at:
* Allowing users to add custom features. Using languages and libraries of their choice. And then letting them glue it into the existing system using just their language and MDL. These plugins could even be compiled and loaded without access to the entire project.
* Allowing multiple versions and implementations of the same plugin to exist. Making rewrites easier, as they can both exist side by side, with developers being able to choose which one they want on the fly.
* Abstracting platform features behind plugins automatically. Plugins for other features will simply be ignored when run on those systems. Features can include operating systems, hardware and software installed, processor features, and anything else.
* Abstrcting interpreter and compiler choice. Language configuration is separate from compiler choices and configuration. Specify custom compilers and interpreters and compare their performance, or choose a stock one.
* Organizing large projects. Organize a project however you see fit with many folder and documentation structures. Overlay your custom plugins on top of an existing plugin system by simply adding a directory to the load list by writing a simple custom start script to wrap the existing one.
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
* Multiplugin, single source code. (Project a single set of source code into many resulting plugins, for example, compiling with different platform flags, and packging all of them.)
* Piecemeal package and download system. (Solving the same problem as the above, compile/choose plugins for a package on the fly as needed.)

Features
==================

__Madz is still in development, features described below (and above) are subject to change, may not be finished, or may never exist (that goes extra for undocumented features that may currently be working)__

Plugin Directories
------------------
Plugins are stored in directories. A plugin system can have multiple directories. Most plugin metadata related to resolution may be stored in it's path.


    the.namespace.of.plugin[1.0.2-alpha+42](an_implementation_name)


The above is a folder name for a plugin with the following metadata:


    name                = "the.namespace.of.plugin"
    version             = "1.0.2-alpha+42"
    implementation_name = "an_implementation_name"


The following are equivalent folder layouts (where '/' represents a folder separator):


    the/namespace.of/plugin/[1.0.2-alpha+42]/(an_implementation_name)
    the.namespace.of.plugin/[1.0.2-alpha+42](an_implementation_name)
    the.namespace.of/[1.0.2-alpha+42]plugin/(an_implementation_name)
    (an_implementation_name)the.namespace.of.plugin/[1.0.2-alpha+42]
    the.namespace.[1.0.2-alpha+42]of.plugin(an_implementation_name)/

Metadata in folder paths must always match the metadata given in plugin descriptions.


Configuration
------------------
Madz, like many complicated systems, provides a multi-layered configuration system. The core concept of the configuration system is that all applicable configurations are merged to compute the current set of options, from which decisions are made. 

There are two primary classes of objects in the configuration system: __Options__ and __Configs__. Options provide a value of some kind, and different kinds of options will have different merge rules. Configs contain both Options and Configs. A Config's merge rules are simple: merge each sub object (which can be Options or Configs). Merge order is often important. Labeled configs include some sort of unique identifier which make sure they are only merged with the matching identifier.

One important consequence of this desgin is how Configs like below are merged:

    # An option using the BaseOption merge strategy: assignment
    class OptionA(BaseConfig): pass
    # An option using the BaseAppendOption merge strategy: append
    class OptionB(BaseAppendOption): pass

    foo = FooConfig([
        OptionA(42),
        OptionB([42]),
        LabeledConfig("label"[
            OptionA(142),
            OptionB([142]),
        ])
    ])

    bar = BarConfig([
        OptionA(99),
        OptionB([99]),
        LabeledConfig("label"[
            OptionA(199),
            OptionB([199]),
        ])
    ])

The results of the merge at each step are listed below:

    result = Config()
    # result.get(OptionA) == None
    # result.get(OptionB) == []

    result = result.merge(foo)
    # result.get(OptionA) == 42
    # result.get(OptionB) == [42]

    result = result.merge(bar)
    # result.get(OptionA) == 99
    # result.get(OptionB) == [42, 99]

    result = result.merge(result.get(LabeledConfig.get_key("label")))
    # result.get(OptionA) == 199
    # result.get(OptionB) == [42, 99, 142, 199]

Note how once the labeled config is added it's simply merged ontop of everything else.

Below are the more global Configs in madz, most of which are applied for the entire duration of the system's execution (listed in the order they would be applied):

* __Default__ - The default config. A psuedo layer since users can't really change it.
* __User__ (unlabeled) - A per machine configuration primarily for providing locations on the system for libraries, headers, compilers, ect. Set via environment variable.
* __System__ (unlabeled) - A per system (of plugins) configuration for providing commands, modes, custom rules for the system, libraries, ect. Set via the startup script.
* __Command__ - A per command configuration. A command isn't a concrete object, rather it's a single call to the system. This describes how to mutate the system.
* __Mode__ (multiple) - A "keyword" which mutates the configuration in specific ways. For example, to choose between debug/production/profiling modes.

Below are the more ephemeral configs in madz, being applied and unapplied rapidly:

* __Plugin__ (unlabeled) - A per plugin configuration for providing plugin specific library imports, optimizations, and build rules. Set via the plugin stub.
* __Library__ (multiple) - A per library configuration, mutating language and compiler configs as necessary.
* __Language__ - A per language configuration.
* __Compiler__ - A per compiler config.

The distinction between labeled and unlabeled Config objects is import but subtle: A labeled object exists entirely within the config system, it has no direct configuration or choice from the user. The user may only indirectly create and apply them through unlabeled Config objects. Unlabeled Config objects represent places where the system is interfacing arbitrary complex information. 

The UserConfig is tied to the complex information passed by the user through the command line. The SystemConfig is tied to the complex information describing the purpose and requirements of the system, and to some extent the user at the command line, the part that is the same as every other team member. The PluginConfig is tied to the complex information that is each plugin.

There are also some special Configs, notably TargetPlatform and SourcePlatform.

Below is a wishlist of configuration features:
* PluginDirectory as an unlabeled Config.
* Generalizing CompilerConfig, or creating new versions of it, for interpreters and VMs.
* Options representing source code declares, (like being able to change A_DEFINE with the config system)
* Better support for multiple platform targeting.

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


