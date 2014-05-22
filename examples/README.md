A collection of examples and basic tests for the madz library.

Examples
------------------
Madz is not currently designed to be used for smaller projects, however there is simple example project in the folder `simple_example` with a readme and a simple project for use.

Tests
------------------
Internal python libraries used by madz are tested using python's unittest framework:

* python_libs\pyext: Examples of the bootstraping python extensions.
* python_libs\pydynecs: Examples of the bootstrapping python ECS.

Using `python -m unittest discover -s python_libs`
