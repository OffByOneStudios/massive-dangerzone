from .parser import *
from .nodes import *
from .base_types import *

class MdlKeywordParseRule(ParseRuleBase):
    default_end_char = ParseRuleChar(char=";")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._nodetype = kwargs["node_type"]
        self._keyword = kwargs["keyword"]
        self._subrules = [[self]] + kwargs["subrules"]

    def _new_levelstate(self, **kwargs):
        return MdlKeywordParseRule.LevelState(**kwargs)

    class LevelState(Parser.ParseStateLevelStack.LevelState):
        def __init__(self, **kwargs):
            self._parent = kwargs["parent"]
            self._subrules = kwargs.get("subrules", [MdlKeywordParseRule.default_end_char])
            super().__init__(**kwargs)

            self._i = 0
            self._rule_order = []

            self._old_rules = []

        def _fixup_parserules(self, state):
            if (self._i == len(self._subrules)):
                self.end_this(state)
                return

            parserules = list(self._special)
            parserules += self._subrules[self._i]

            # Set parse rules
            state[Parser.ParseStateRules.key()].value = parserules

        def parsed(self, state, accepted):
            for rule in self._subrules[self._i]:
                if accepted.rule is rule:
                    self._i += 1
                    break

            self._rule_order.append(rule)
            self._fixup_parserules(state)

        def start(self, state):
            self._special = state[ParseStateSpecialRules].all()
            self._old_rules = state[Parser.ParseStateRules.key()].value

            self._i = 1
            self._rule_order.append(self._parent)
            self._fixup_parserules(state)

        def end(self, state):
            state[Parser.ParseStateRules.key()].value = self._old_rules
            state[ParseStateParseTree.key()].add_root()

        def _copy(self, new):
            super()._copy(new)

            new._i = self._i
            new._rule_order = list(self._rule_order)

            new._special = self._special
            new._old_rules = self._old_rules

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        kwargs["subrules"] = self._subrules
        return super()._gen_levelargs(state, **kwargs)

    def _do_parse(self, pstro, state, gen_args):
        if not pstro.match(self._keyword, case_insensitive=True):
            return "No Keyword"

        state[ParseStateParseTree.key()].current_root = self._nodetype()

class MdlParseSymbol(ParseRuleBase):
    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, string.ascii_letters)

        res = pstro.parsed()
        if len(res) == 0:
            return "Symbol must have more than 0 charaters."

        state[ParseStateParseTree.key()].current_root.name = res

class MdlParseType(ParseRuleBase):
    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, string.ascii_letters)
        if len(pstro.parsed()) == 0:
            return "Type must have more than 0 charaters."

def main():
    import sys

    specialrules = ParseStateSpecialRules(
        whitespace=ParseRuleNameMod("whitespace", ParseRuleWhitespace()),
        comment=ParseRuleNameMod("comment", ParseRuleFromTillEndOfLine(char="#")))

    rule_symbol = ParseRuleNameMod("Symbol", MdlParseSymbol())
    rule_type = ParseRuleNameMod("Type", MdlParseType())
    rule_eol = ParseRuleNameMod("EOL", ParseRuleChar(char=";"))
    rule_typedef = ParseRuleNameMod("Type", MdlKeywordParseRule(
        keyword="type",
        node_type=TypeDeclaration,
        subrules=[
            [rule_symbol],
            [rule_type],
            [rule_eol],
        ]
        ))
    rule_variable = ParseRuleNameMod("Var", MdlKeywordParseRule(
        keyword="var",
        node_type=VariableDefinition,
        subrules=[
            [rule_symbol],
            [rule_type],
            [rule_eol],
        ]
        ))

    parser = Parser(
        specialrules.all() + 
        [
            rule_typedef,
            rule_variable,
        ],
        [
            specialrules,
            ParseStateParseTree(),
        ])
    rstate = parser.parse(open(sys.argv[1], 'r').read())

    print(rstate[Parser.ParseStateDebugStack.key()])
    print(rstate[ParseStateParseTree.key()])
