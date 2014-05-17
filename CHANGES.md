
Version 0.5.0
=============

* Adding new python libraries:
    * pyext: Python extensions.
    * pydynecs: A dynamic python based Entity Componenet System.
* Refactoring madz in preperation for bootstrapping.

Version 0.4.0
=============

* Rebuilt as a live daemon/client architecture.
    * Command, kill, execute, search, and (optional) ipython functions.
    * Cleaned up logging output.
* Added new execution model.
* New requirement: pyzmq.

Version 0.3.2
-------------

* Improved file manipulation infrastructure.
* Various compiler and bug fixies.

Version 0.3.1
-------------

* Improved compiler infrastructure.
    * Adding support for rudimentary architecture detectiong.
    * Refactoring compilers and languages relationships (new: many compilers to many languages, used to be: many compilers to one language).
* Improving support for mdl, namely custom mdl loaders, including ability to place into a file.

Version 0.3.0
=============

* Adding MDL parser.
* Improving documentation.
* Improving python/c/c++ wrapper and compiler layers.

Version 0.2.0
=============

* Refactored folder layout.
* Added Config system.
* Reworked imports.
* Refactored actions.
* Refactored languages.
* Reworked MDL validation.
* Various bug fixes.