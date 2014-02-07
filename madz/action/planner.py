from .. import HTN
from .. import operating_system
import abc

class LoadProvider(object):
    """Temporary placeholder for future load providers."""
    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub
        self.operating_system = operating_system.get_system()

    def get_dependency(self):
        return False

    def do(self):
        self.operating_system.load(self.plugin_stub)


class PluginOperationBase(MethodBase):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)

    def get_provider(self, term):
        plugin = term.args["plugin"]
        if term.typename == "wrap":
            return plugin.language.make_wrapper()
        if term.typename == "build":
            return plugin.language.make_builder()
        if term.typename == "load":
            return self.LoadProvider(plugin)
        return None


class PluginOperation(PluginOperationBase):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)

    def precondition(self, term, state):
        provider = self.get_provider(term)

        if bool(provider.get_dependency()):
            return None
        return {'provider': provider}


class PluginNullOperation(PluginOperationBase):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)

    def precondition(self, term, state):
        provider = self.get_provider(term)

        if not bool(provider.get_dependency()):
            return None
        return {}


class PluginOperationExpand(PluginOperationBase):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)

    def precondition(self, term, state):
        plugin = term.args["plugin"]
        if term.typename == "wrap":
            return plugin.language.make_wrapper()
        if term.typename == "build":
            return plugin.language.make_builder()
        if term.typename == "load":
            return self.LoadProvider(plugin)
        return None


def build_planner(**kwargs):
    terms = kwargs.get("terms")
    op = PluginOperation(terms=terms)
    op_null = PluginNullOperation(terms=terms)
    op_expand = PluginOperationExpand(terms=terms)

    planner = HTN.Executer()
    planner.rules.add(op)
    planner.rules.add(op_null)
    planner.rules.add(op_expand)

    planner.priority = PriorityShortCircut([
        PriortityRank([
            (10, op_null),
            (6, op),
            (4, op_expand),
        ])
    ])

    return planner

def main():
    planner = build_planner()

    plan = planner.buildPlan(init_terms = [HTN.Term("build", plugin=2)])

    print(plan)

    planner.executePlan(plan)l