pyExt
==================

### Version: 0.1.4

Summary
------------------

pyExt is a library for python providing extensions to the core language which madz will provide during bootstrapping. This library is an attempt to ease bootstrapping by providing madz features ahead of time via pure python implementation.

Features
------------------

The Features provided by this library currently:

* Class properties (oversight of python core)
* Contexts (thread local global variables)
* Events (lists of callables)
* Imposters (specifically for python modules)
* Multimethods (ala clojure/common lisp)
* Tasks (for managing multiple tasks; potentially with threads)
* pyZMQ extensions

Future potential features:

* Latebinding variables.
* Eventhubs (a global singletone for managing large numbers of Event objects).
* An extended class metaclass (for better class compisition).

