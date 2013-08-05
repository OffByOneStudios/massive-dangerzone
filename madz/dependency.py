"""dependency.py
@OffbyOneStudios 2013
Code to create and traverse dependency graphs of plugins.
"""

import os.path, time

class Dependency(object):
    """Generates a dependency graph of plugins allowing for generation in the correct order."""

    def __init__(self, dependencies, targets):
        self.dependencies = dependencies
        self.targets = targets

    def check(self):
        """Checks that there are no targets which are older than the dependencies."""
        newest_dependency = time.ctime(0)

        #Find the newest dependency
        for d in self.dependencies:
            temp = time.ctime(os.path.getmtime(d))
            if temp > newest_dependency:
                newest_dependency = temp

        unsatisfied_targets = []

        #Verify each target is newer than the newest dependency, add targets
        #which are older than their dependences to the unsatisfied_targets list
        for t in self.targets:
            if os.path.isfile(t):
                if time.ctime(os.path.getmtime(t)) >= newest_dependency:
                    unsatisfied_targets.append(t)
            else:
                unsatisfied_targets.append(t)
        self._unsatisfied_targets = unsatisfied_targets

    def __bool__(self):
        self.check()
        if len(self._unsatisfied_targets) == 0:
            return True
        else:
            return False

    __nonzero__ = __bool__

    def get_unsatisfied_targets(self):
        return self._unsatisfied_targets

"""
#Example calls to Dependency

Dep = Dependency(["loader.py"],["builder.py"])

print Dep.get_unsatisfied_targets()

if Dep:
    print "hi"
"""
