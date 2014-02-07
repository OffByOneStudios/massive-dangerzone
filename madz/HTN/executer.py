from .state import *
from .terms import *
from .rule import *
from .priority import *

class Executer(object):
    def __init__(self):
        self.initialPlanState = [TermsState]
        self.initialExecuteState = StateCollection([])
        self.priority = PriorityShortCircut([])
        self.rules = set()

    def initialPlanState():
        doc = "The initialPlanState property."
        def fget(self):
            return self._initialPlanState
        def fset(self, value):
            self._initialPlanState = value
        return locals()
    initialPlanState = property(**initialPlanState())

    def initialExecuteState():
        doc = "The initialExecuteState property."
        def fget(self):
            return self._initialExecuteState
        def fset(self, value):
            self._initialExecuteState = value
        return locals()
    initialExecuteState = property(**initialExecuteState())

    def priority():
        doc = "The priority property."
        def fget(self):
            return self._priority
        def fset(self, value):
            self._priority = value
        return locals()
    priority = property(**priority())

    def rules():
        doc = "The rules property."
        def fget(self):
            return self._rules
        def fset(self, value):
            self._rules = value
        return locals()
    rules = property(**rules())

    def _stateValid(self, state):
        return state[TermsState].lengthOfTerms() != 0

    class RulesTermCache(object):
        def __init__(self, rules, priority):
            self.rules = sorted(rules, key=priority_to_key(priority))
            self._rule_cache = {}

        def __getitem__(self, key):
            if key in self._rule_cache:
                return set(self._rule_cache[key])
            
            res = set()

            for rule in self.rules:
                if key.typename in rule.term_typenames:
                    res.add(rule)

            self._rule_cache[key] = res
            return set(res)

    class StackElement(object):
        def __init__(self, rules, state):
            self._rule = rules[0]
            self._state = state.copy()
            self._remaining_rules = rules[1:]

        @property
        def current_rule(self):
            return self._rule[0]

        @property
        def current_precond(self):
            return self._rule[1]

        @property
        def state(self):
            return self._state

        def next(self):
            if len(self._remaining_rules) == 0:
                return False
            self._rule = self._remaining_rules.pop()
            return True

    def _testRule(self, rule, term, state):
        try:
            return (rule, rule.precondition(term, state))
        except:
            return None

    def _applyRule(self, term, stack_element, state):
        stack_element.current_rule.postcondition(term, state, stack_element.current_precond)

    def buildPlan(self, **kwargs):
        ## Build initial state:
        state = StateCollection([m(**kwargs) for m in self.initialPlanState])
        rules = Executer.RulesTermCache(self.rules, self.priority)
        stack = []
        backtracking = False
        trytop = False

        print (state[TermsState]._terms)

        ## Execute loop
        while self._stateValid(state):
            print ("Loop[Backtrack: {}, Trytop: {}] = {}".format(backtracking, trytop, state[TermsState].currentTerm))
            if backtracking:
                # make sure we can backtrack
                if len(stack) == 0:
                        raise Exception("No computeable plan.")
                # We are backtracking.
                if (stack[-1].next()):
                    # If we have a next element, try it.
                    state = stack[-1].state.copy()
                    backtracking = False
                    trytop = True
                    continue
                else:
                    # otherwise, backtrack some more.
                    stack.pop()
                    continue
            else:
                # We are trying to resolve terms
                term = state[TermsState].currentTerm
                if not trytop:
                    # The valid rules for the term
                    valid_rules = rules[term]

                    # Calculate the rules passing the precondition
                    possible_rules = map(lambda r: self._testRule(r, term, state), valid_rules)
                    possible_rules = filter(lambda r: not (r[1] is None), possible_rules)
                    possible_rules = list(possible_rules)

                    # We ran out of possibilities, back track and try again
                    if len(possible_rules) == 0:
                        backtracking = True
                        continue

                    # Push it onto the backtracking stack
                    stack.append(StackElement(possible_rules, state))
                else:
                    trytop = False

                # Apply rule
                self._applyRule(term, stack[-1], state)

        execute_rules = list(map(lambda se: (se.current_rule, se.current_precond, se.state), stack))

        return execute_rules

    def executePlan(self, plan):
        state = self.initialExecuteState.copy()
        for (rule, precond, rule_state) in plan:
            try:
                rule.execute(state, precond)
            except:
                print("Execute failed")
                break

