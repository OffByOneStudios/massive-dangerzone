pyDynECS
==================

### Version: 0.1.0

Summary
------------------

pyDynECS is a python implementation of a dynamic entity component system. Specifically designed for building well defined dynamic objects via a component system, as opposed to optimizations via component seperation found in many ECS used in, for example, games. Eventually this library will be merged into the MADZ system as a set of modules, and mixed with more efficient ECS libraries, hopefully building a generalized ECS library capable of powerful features and efficient optimizations, (although perhaps not both at once).

Requires:
* pyExt

Features
------------------

The primary purpose of this is to provide the features for the following 3 libraries within madz:

* Module Descriptions (D): A way to hold component data about modules, manage the different feature setys availble and index them.
* Identity (I): Provide the basis for an identity system.
* Nodes (N): Provide the basis for a node system, like parse trees.

The following features will be provided by this library:

* Core [DIN]
    * Entity Component System declarations (with various pruposes).
    * Entity Allocation and Indexing Schemes.
    * Component Manager declarations.
        * With component dependencies.
    * Syntax helpers for hooking the above togeather.
        * Entity Wrapper classes.
* Entity Types [DIN]
    * Creating types of entities based off of required componenets.
        * Including multiple types, with similar component structures.
    * Indexing and listing features for these types, without an actual full component manager.
    * Helpers for constructing these entity types.
* Tree/Graphs [D_N]
    * Creating graphs and trees with entity referential components.
* Computed Components [DIN]
    * Computing components from other components.
    * Lazy versions.
* Serialization [_IN]
    * Methods for serializing the ECS.
    * Multiple outputers for the inmemory serialized format.
    * Inputters for on disk to inmemory serialized format.
    * Requires a fully declared system with the appropriate types.

Organization
------------------

The following is the organization of the pyDynECS library:

* abstract: Abstract Base Classes.
* core: Core feature implementations.
* entityclass: Entitiy class features.
* entitygraph: Graphs and trees from components refrencing entities.
* managers: Extended and specialized types.
* serilization: Serialization implementations.
* syntax: Syntax wrappers.
