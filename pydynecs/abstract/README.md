pyDynECS/abstract
==================

These are the abstract base classes for the pyDynECS library. These describe the basic layout of core abstractions used throughout the library.

Definitions
------------------

* __Entity__: An entry in the system.
* __Manager__: Manages some information within the system.
* __Processor__: Manages the execution of some aspect of the system. (Some ECS implementations refer to these as systems).
* __System__: The collection of Entities, Managers, and Processors.
* __Class__: A definition of a class of entities, defined in an ontological sense (as opposed to a taxonomy). Can provide additional components and functionality. Used as a halfway point towards implementing Processors, but in a dynamic system is a powerful addition.

Abstract Interfaces
------------------

* `IEntity`
    * Provides a standard interface for providing an object for equality testing and hashing for entities, and entity facades, amoung others.
* `IEntityAllocator`
    * An interface for creating new entities.

* `IEntityManager`
    * Provides a base interface for managers. Specifically for dependencies and entity-manager membership.
* `IComponentManager`
    * Implements: `IEntityManager`
    * Provides a base interface for mapping entities to data.
* `IIndexManager`
    * Implements: `IEntityManager`
    * Provides a base interface for mapping data (indecies) to entities.

* `IPartitionManager`
    * __PROPOSED__
    * Implements: `IEntityManager`
    * Provides a base interface partition entities for use with processes/classes.

* `ISystem`
    * Implements: `IEntityAllocator`
    * Provides a base interface for system implementations.