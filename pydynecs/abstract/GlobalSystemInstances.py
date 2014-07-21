"""pydynecs/abstract/GlobalSystemInstances.py
@OffbyOne Studios 2014
Global store of system instances.
"""

import os
import sys

system_instances = {}

_next_instance_id = 0
def next_instance_id(self):
    global _next_instance_id
    t = (os.getpid(), _next_instance_id)
    system_instances[t] = self
    _next_instance_id += 1
    return t
