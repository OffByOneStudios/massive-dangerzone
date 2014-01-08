from .abstract_bases import *
from numbers import Number

###
### Helpers
###

class ParseString():
    def __init__(self, v):
        self.v = v
        self._i = 0
        self._l = len(v)

    @property
    def cur(self):
        if self._i is None:
            return None
        return self.v[self._i]

    @property
    def lka(self):
        if self._i is None:
            return None
        return self.v[self._i + 1]

    def p(self):
        self._i += 1
        if self._i >= self._l:
            self._i = None
        return self.cur

    def parsed(self):
        if self._i is None:
            return self.v
        return self.v[:self._i]

    def test_in(self, tstr):
        cur = self.cur
        if cur is None: return None
        return cur in tstr

    def match_all(self, tstr):
        while (self.test_in(tstr)): self.p();
        return True;

    def match(self, matchstr, case_insensitive=False):
        lm = len(matchstr)
        matching = self.v[self._i:self._i + lm]

        if (case_insensitive):
            matching = matching.lower()
            matchstr = matchstr.lower()

        if (matching != matchstr):
            return False
        else:
            self._i += lm
            return True

###
### Parser
###

class Parser():
    class ParseStateRules(ParseStateValue):
        @classmethod
        def _value_valid(cls, value):
            if Parser._valid_parse_rules(value) != False:
                return True
            return False

        def _value_copy(self):
            return list(self.value)

        def _value_init(self):
            return list()

    class ParseStateDebugStack(ParseStateStack):
        @classmethod
        def _valid_value(cls, value):
            return True

        def __str__(self):
            return "ParseStateDebugStack:\n{}".format("".join(
                map(lambda s: "{}{!s}:  {!r}\n".format("  "*(s[1]+1), s[0], s[0].parsed_string), self._stack)))

    class ParseStateLevelStack(ParseStateStack):
        class LevelState(object):
            def __init__(self, **kwargs):
                self.__reinit = kwargs
                self._start = kwargs.get('on_start', lambda self, state: None)
                self._end = kwargs.get('on_end', lambda self, state: None)
                self._parsed = kwargs.get('on_parsed', lambda self, state, accepted: None)

            def parsing(self, state):
                pass

            def parsed(self, state, accepted):
                self._parsed(self, state, accepted)

            def start(self, state):
                self._start(self, state)

            def finish(self, state):
                self.__state = state
                state[Parser.ParseStateLevelStack.key()].pop()

            def do_end(self):
                self.end(self.__state)

            def end(self, state):
                self._end(self, state)

            def _copy(self, new):
                pass

            def copy(self):
                new = self.__class__(**self.__reinit)
                self._copy(new)
                return new

        @classmethod
        def _valid_value(cls, value):
            if isinstance(value, Parser.ParseStateLevelStack.LevelState):
                return True
            return False

        def pop(self):
            popped = super().pop()
            popped.do_end()
            return popped

    def __init__(self, parse_rules, state_objects):
        parse_rules = self._valid_parse_rules(parse_rules)
        state_objects = self._valid_state_objects(state_objects)

        if (parse_rules is False) or (state_objects is False):
            raise Exception("Invalid parse table.")

        self._parse_rules = parse_rules
        self._state_objects = state_objects

    @staticmethod
    def _valid_parse_rules(parse_rules):
        if not isinstance(parse_rules, list):
            return False
        for r in parse_rules:
            if not isinstance(r, IParseRule):
                return False
        return parse_rules

    @staticmethod
    def _valid_state_objects(state_objects):
        if isinstance(state_objects, list):
            state_objects = {v.key(): v for v in state_objects}

        for k, v in state_objects.items():
            if not isinstance(v, IParseState) or v.key() != k:
                return False
        return state_objects

    def _setup_parse(self):
        new_state = dict(self._state_objects)
        
        return new_state

    def _do_rules(self, pstr, state):
        #=== Parse
        #= Clean up parse state
        accepted = []
        errored = []

        #= Find best (longest) matching rule
        for rule in state[Parser.ParseStateRules.key()].value:
            result = rule.try_parse(pstr, IParseState.copy_state(state))
            if result != None:
                if result.valid:
                    accepted.append(result)
                else:
                    errored.append(result)

        if len(accepted) == 0:
            raise Exception("No matching valid parse possible:\n{!r}\n Errors:\n{!s}\n {!s}".format(
                pstr[:80],
                "".join(map(lambda r: "  {!s}: {!s}\n".format(r.rule, r), errored)),
                state[Parser.ParseStateDebugStack.key()]))

        return sorted(accepted, key=lambda a: len(a.parsed_string), reverse=True)

    def parse(self, pstr):
        state = self._setup_parse()
        parse_rules = list(self._parse_rules)

        pstr = str(pstr)
        
        state[Parser.ParseStateLevelStack.key()] = Parser.ParseStateLevelStack()

        state[Parser.ParseStateRules.key()] = Parser.ParseStateRules()
        state[Parser.ParseStateRules.key()].value = parse_rules

        state[Parser.ParseStateDebugStack.key()] = Parser.ParseStateDebugStack()

        # Parse loop
        while (pstr != ""):
            #= Inform level
            top_level = state[Parser.ParseStateLevelStack.key()].top
            if not (top_level is None):
                top_level.parsing(state)

            try:
                accepted = self._do_rules(pstr, state)[0]
            except Exception as e:
                print("Might need to backtrack!")
                raise e #todo, partial parse! backtrack!

            #=== Build next parse state
            state = IParseState.copy_state(accepted.state)
            state[Parser.ParseStateDebugStack.key()].push((accepted, len(state[Parser.ParseStateLevelStack.key()]._stack)))

            #= Inform level
            top_level = state[Parser.ParseStateLevelStack.key()].top
            if not (top_level is None):
                top_level.parsed(state, accepted)

            #= Change level (new parse rules, node assembly, etc.)
            new_level = accepted.new_level
            if not (new_level is None):
                new_level.start(state)
                state[Parser.ParseStateLevelStack.key()].push(new_level)

            #= String update
            astr = accepted.parsed_string
            if not pstr.startswith(astr):
                raise Exception("Invalid parse string: {}".format(astr))
            pstr = pstr[len(astr):]

        return state


            #new_parse_rules = accepted.generate_parse_rules()

            #if isinstance(new_parse_rules, list):
            #    state[Parser.ParseStateRuleStack.key()].push(new_parse_rules)
            #elif isinstance(new_parse_rules, Number):
            #    num = int(new_parse_rules)
            #    while (num < 0):
            #        state[Parser.ParseStateRuleStack.key()].pop()