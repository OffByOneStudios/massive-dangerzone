
## Ontological Object Semantics

Object systems, that is the object semantics of languages (including the code generation and runtime features required for objects), are a common abstraction within modern programming languages. There are many variations of object systems, and the semantics that build them. We describe here an attempt to build an ontologically based object system, including the semantics to use it, which will provide a superset of other object systems in one total system.

### What are objects?

The point of object systems is of course to provide the semantics for our desire to reason about things. To do this many object systems provide classes, a description (often itself represented using some sort of object) of what a class of instances look like. Because classes may share functionality we use inheritence to create classes describe the broad range of functionality, and then inheirt that class into the more specific instance. This is similar to classical categorization theory done, for example, in taxonomies of animals.

However, recent advances in categorization theory, including research on the way humans think, has lead us to better systems of describing classes, and their relationships. It's time to bring these advances to programming. But first an intution of what the system will do is required. We are going to define a new vocabulary because in some cases we will need to refer to typical object systems, as we will be using them to implement the ontological object system, hence we will attempt to avoid conusion betweem them in naming.

Instances are what we typically refer to as objects, an instance is a collection of information about a thing, each piece of information is called an aspect. Kinds describe constraints which instances must fit to be considered to be of that kind, metaphorically similar to classes (and like classes, are themselves instances within the ontology). Aspects can contain complex values, including objects, other instances and kinds, and can be applied to both kinds and instances, metaphorically similar to private members.

One of the key insights of ontologies is that actual instances of kinds are often widly divergent from what we consider to be the "typical" instance, from which we tend to base our classical categorizations on, it's when "atypical" instances are found that taxonomies break down, but ontologies continue to function: just because some kinds no longer apply, others will work just fine, in addition, others may become recognized. This leads to new concepts within the ontological object system which are important to discuss:

* As instances are just collections of aspects, the kind(s) of an instance can shift over the lifetime of the instance as aspects are modified, compilers can also also easily infer these kind changes and optimize approprietly if possible. We strongly suspect this is a dynamic equivelent of type systems using <trait?>.
* Constracting (or modifying) an instance to appear like an typical manifestation of a kind is the primary structured way of creating (or expanding) an instance of (to) a particular kind (i.e. instead of merely adding the aspects by hand). This is similar to constructors, except they are purely static functions with no special behaviour.
* Kinds can be recursively defined, such that an instance with aspects describing other instances, may manifest a kind be merely refrencing it via a specific aspect.
* Kinds can also be modified, by changing aspects of kinds (most often by mutating them) kinds can aquire additional behaviour. While messy, appropriately constructed abstracts can safely encapsulate this within other semantics.

The final important concept required to understand the behaviour the system is relationships. Relationships (like kinds) are instances (and hence of kinds) which describe how instances (and hence kinds) are related. Relationships are an important concept because one aspect could define a dizzying array of relationships. Relationships can have many special features, for example many are invertable (i.e. they have a direction, hence they can be reversed).

The Ontological Object system we describe will be designed to include the instances (kinds, and relationships) required to provide many features. Interestingaly, semantics can be added simply by adding the required instances to the ontological system. An unmentioned, so far, topic is efficiently organizing this system such that it can be competitive with exisiting object systems, while we believe this challenge is entirely secondary to understanding the ontological object system, we will make note of it's considierations where applicable. Hence we will discuss some useful kernels for creating the ontological system (and efficiently organizing it) within the implementation section.

### Entity Component System Usage

It's notable that Ontologies are similar to entity component systems. Indeed, we will be basing our implementation design off of entity component systems. The metaphorical equivelents to be aware of:

* An **Entity** is an **Instance**.
* A **Component** is an **Aspect**.
* An **EntityClass** is similar to a **Kind** (in that it provides features for entities fiting certain conditions).

Our implementation, and design of features within the ontological object system, rely on the entity component system for important features:

* State Transactional Memory (and Thread Safety): This is almost entirely the responsibility of the entity component system, the ontological object system wraps the exisiting semantics, and ingrains it in it's helper/extended semantics. Ditto the thread safety of using the memory in the entity component system.
* Kind Optimization: While the ontological system is responsible for reasoning about kinds (like complete subsets, etc.) the entity component system is responsible for it's optimization over aspects and instances, extensions to the ontological object system may have to provide optimization to their specific feature set via the entity component system (if it's low enough level, for example).
* Events: Like state transactional memory, the entity component system is responsible for triggereing notifications of data changed (after it's happened). It is not responsible for providing ways to guard data or verify transactions, although those will operate at the entity component system layer, and may be third part extensions for the entity component system, rather than core implementation details of the ontological object system.

### Self Optimizing

It is possible to implement optimizing features within the ontological system itself. However limitations of our inital implementation will likely prevent that.

## Implementation Design

We will describe our implementation design for the ontological object system using python syntax. The design here assumes a singular ontological object system, support for multiple systems will require a user to deal with the negotiation between them by hand.

### Globals

There are some global variables used to provide access into the system.

* OntologicalObjectSystem: This class provides the context variables used to choose the system to talk about, unlike the entity component system design, the object does not gracefully deal with being manipulated, while the current variable can be changed, already created objects may completely ignore it, or may fail to function completely.
    * OntologicalObjectEntityComponentSystem (variable ECS): This is the entity component system which provides the majority of the data storage features, the ontological object system is built completely ontop of the assumptions provided by this.

### Notable Design Choices

Here we describe some design choices to be aware of:

#### Declaration as Usage

Most modern object systems have two seperate steps for using objects, first declaring the class, then using the class (often within a part of the declaration of another class). Many object systems treat the declaration of a class *as* usage, except with special syntax. In our case we will attempt to use exisiting declaration syntax, via metaclasses, to provide a similar experience, even if the same thing could be just as easily achieved without it.

#### Symbols as Identity

A common dynamic object choice is to use strings for object keys, while we recognize the utility of doing this, and we provide support for it, we prefer to use the languages exisitng namespacing/module infrastructure for providing symbols, and hence namespaces for them.

### Usage:

Below we provide some examples of how to use the ontological object system. These examples are in python.

```python
# Here we show a function we operates on an ontological object instance:

import pyont

from a_library.using.ontological_objects import *

def a_function(instance, a_str_arg):
    # First we do guard checks:
    a_str_arg = str(a_str_arg)
    instance = pyont.ensure(instance, KindFoo) 
    
    # Next we do the operation
    instance.a_kind_foo_func(a_str_arg)

    # Now we return some instance aspect (state potentially modified by the above function)
    return KindFoo.some_state
    
```

This relatively simple example shows how the ontological object system isn't that different than a normal object system. We can have objects which we can call functions on, return variables from, and ensure are the right type.

`ensure` (in the pyont library) is used to ensure that an instance `is-a` kind, that is that it expresses the `is-a` relationship kind, it is similar to an `isinstance` check followed by throwing an exception, but is more precisely equivelent to the `str` type coerce function.

The first major thing about this code to notice is that it does make heavy use of helper syntax, we will breifely delve into that syntax to disect what is happening.

First we call `pyont.ensure` this is likely the most complicated piece of syntax. Essiently this function is putting forward the proposal that `instance` `is-a` `KindFoo`, either the system finds a way to agree with that statement or it rejects it and raises an exception. The returned value is basically the same object, except that it has hints to the resolution system about which things we are looking for, the assignment is technically unneccessary, but may improve performence, error reports, and discoverability.

The `pyont` namespace is designed to a helper syntax import. Hence `ensure` is actually misleading. The real name for it should be `pyont.base.rel_is_a.ensure`, which is actually an aspect of the `is-a` relationship kind, with roughly the following code:

```python

@...
class rel_is_a(...):
    ...
    
    @...
    def ensure(instance, kind):
        # Make sure instance is actually a valid ontological instance
        instance = system.ensure_instance(instance)
        
        result = system.solver.submit(system.make_relationship(rel_is_a, instance, kind))
        
        if result.fail:
            raise IsNotAException(instance=instance, kind=kind, solver_result=result)
        
        return system.syntax.instance(instance, prefer=[kind])
```

### Initial System:

Now that we have described the syntax, we can describe the initial included relationships and instances:



## Comparisons

Below we compare the ontological object system to other common paradigms. As the ontological system attempts to be a superset, we describe how such a feature can be provided by the system.

### CLOS

CLOS (Common Lisp Object System) 

#### Slots

[0](http://stackoverflow.com/questions/629631/slots-in-clos)

The CLOS slots are the basic inspiration for the way the helper syntax for described aspects of kinds.

### Haskell

[0](http://www.haskell.org/haskellwiki/OOP_vs_type_classes)

