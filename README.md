Massive Dangerzone
==================

### Version: 0.5.0-dev ([CHANGES](https://github.com/OffByOneStudios/massive-dangerzone/blob/master/CHANGES.md))

Summary
------------------

Massive-Dangerzone, abbreviated madz, is an extensible module management system built on python. Modules can be written in any programming language, against any runtime, for any platform, to do this, these platform requirements, and implementations, are gathered into a forge, which can transform the module's source code into a binary (or, theoretically, any target). Modules communicate through any method both their forges support (for example, via their CFFIs). Modules can have additional code generated for them from their source code, or the source code of their dependencies, a specific example is MDL (Madz Description Language) which describes to madz what each module does (although theoretically, a language parser could do this as well). This description is then used to generate header files for linking and editing.

To achieve this cross platform goal, madz provides a framework for compilers, debuggers, languages, runtimes, etc. In addition madz provides a variety of other features, or frameworks for features, including a build system using 'AI' planning (as opposed to simple dependency tress), project file generation, executable launching, debugging, and deployment, a powerful report system (logs with interactive 'live' objects), among other potential features.

**This codebase is still a work in progress, indeed this project is as much research as it is development.**


## Installation 
See https://github.com/OffByOneStudios/massive-dangerzone/blob/master/INSTALL.md