
## Identity

If we are going to have a bunch of modules laying around it's important to be able to talk about identity. How do we identify this data we have?

### Context

It's important to realize that when people want to refrence a piece of data there is often some piece of context they are working from.

* `When we browse folders we manipulate a current working directory.`

And from that we can make a system which is able to keep context in mind when refrencing other things, and supply this context on introspection, or errors occur.

### Types

There are also different types of identity, which have different properties, some identities fit into more than one category:

* Global Unique Identity: Values, computed (hash of data) or assigned (GUID), which are gaurnteed to be unique. These can be very useful for the systems which manipulate modules to use to quickly manipulate identities and modules.
* Human Usable Identity: Values which are created for human consumptions, namespaces, implementation names, codenames, tags, generated names.
* Content Identity: Values computed from the contents of the module, for example abstraction names, concreate object names, types, dependent modules.
* Group Identity: Values which describe collections of identites like authors, libraries, and namespaces.
* Versioning Identity: Values which describe the differences between otherwise similar data, version numbers, commit parents, hashes.

We will attempt to describe the various types of data and how we can organize them.

#### Namespace

This is the most common way of organizing code. Over the years a number of different techniques have been made in attempts to create namespacing schemes. For example Java's web oriented reverse domain name scheme.

#### Version

There have been a number of versioning systems over the years. From simple number incrementing to trees of versioning.
