import madz.pyMDL.plugin_types as base_types

class TypeObject(base_types.TypeType):
    def __init__(self, parents=[], members={})
        self.parents = parents
        self.members = members
        self._hash = hash(hash(tuple(sorted(members.iteritems()))),
                          hash(tuple(parents.iteritems())))

    def __eq__(self, other):
        return (self.parents == other.parents and self.members == other.members)

    def __hash__(self):
        return self._hash

    def canonical_member_ordering(self):
        def order_key(t):
            name, node = t

            prim_order = 2

            if isinstance(node, base_types.TypeFunction): prim_order = 1

            return (prim_order, name)

        return sorted(self.members.iteritems(), key=order_key)

    def validate(self):
        #ensures that parents are other types
