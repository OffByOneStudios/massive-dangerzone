from .parser import *
from .nodes import *
from .base_types import *

class MdlParserConfig():
    def __init__(self, config):
        self.config = dict(config)
        #symbol_chars
        #symbol_first_chars
        #typerule

class MdlParseRuleBase(ParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._config = kwargs.get("config", MdlParserConfig({}))

class MdlKeywordParseRule(MdlParseRuleBase):
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

            new._parent = self._parent
            new._special = self._special
            new._old_rules = self._old_rules

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        kwargs["subrules"] = self._subrules
        return super()._gen_levelargs(state, **kwargs)

    def _do_parse(self, pstro, state, gen_args):
        if not pstro.match(self._keyword, case_insensitive=True):
            raise Exception("No Keyword")

        state[ParseStateParseTree.key()].current_root = self._nodetype()

class MdlParseSymbol(MdlParseRuleBase):
    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, self._config.config["symbol_chars"], self._config.config["symbol_first_chars"])

        res = pstro.parsed()
        if len(res) == 0:
            raise Exception("Symbol must have more than 0 charaters.")

        state[ParseStateParseTree.key()].current_node.name = res

class MdlTypeLevelParseRule(MdlParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._modrules = kwargs["modrules"]
        self._typerules = kwargs["typerules"]

    def _new_levelstate(self, **kwargs):
        return MdlTypeLevelParseRule.LevelState(**kwargs)

    class LevelState(Parser.ParseStateLevelStack.LevelState):
        def __init__(self, **kwargs):
            self._parent = kwargs["parent"]
            self._rule_order = []
            super().__init__(**kwargs)

        def parsed(self, state, accepted):
            if accepted.rule in self._parent._typerules:
                self.end_this(state)

            self._rule_order.append(accepted.rule)

        def start(self, state):
            self._old_rules = state[Parser.ParseStateRules.key()].value
            self._old_func = state[ParseStateParseTree.key()].get_current_node_func()

            parserules = list(state[ParseStateSpecialRules].all())
            parserules += self._parent._modrules
            parserules += self._parent._typerules

            state[Parser.ParseStateRules.key()].value = parserules

        def end(self, state):
            state[Parser.ParseStateRules.key()].value = self._old_rules
            state[ParseStateParseTree.key()].set_current_node_func(self._old_func)

        def _copy(self, new):
            super()._copy(new)

            new._rule_order = list(self._rule_order)

            new._special = self._special
            new._old_rules = self._old_rules
            new._old_func = self._old_func

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        return super()._gen_levelargs(state, **kwargs)

    def _do_parse(self, pstro, state, gen_args):
        pass

class MdlTypeParseRuleBase(MdlParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._nodetype = kwargs["nodetype"]
        self._keyword = kwargs["keyword"]

    def _do_parse(self, pstro, state, gen_args):
        if not pstro.match(self._keyword, case_insensitive=True):
            raise Exception("No Keyword")

        state_parsetree = state[ParseStateParseTree.key()]
        state_parsetree.current_node.type = self._nodetype()
        state_parsetree.set_current_node_func(lambda r, current_func=state_parsetree.get_current_node_func(): current_func(r).type)

class MdlTypeParseRuleComplex(MdlParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__kwargs = kwargs
        self._chars = kwargs["chars"]
        self._nodetype = kwargs["nodetype"]
        self._subnodetype = kwargs["subnodetype"]
        self._endrule = self._end_rule()

    def _end_rule(mself):
        class EndRule(MdlParseRuleBase):
            mchars=mself._chars
            mname=mself._name
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                _name = ("" if self.mname is None else self.mname) + "!End"

            def _do_parse(self, pstro, state, gen_args):
                if not pstro.match(self.mchars[1]):
                    raise Exception("No close Symbol")
        return EndRule()

    def _name_rule(mself):
        class SymbolRule(MdlParseSymbol):
            msubtype = mself._subnodetype
            mname=mself._name
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                _name = ("" if self.mname is None else self.mname) + "!Symbol"
            def _do_parse(self, pstro, state, gen_args):
                state[ParseStateParseTree.key()].current_node.get_complex_list().append(mself._subnodetype())
                state[ParseStateParseTree.key()].set_current_node_func(lambda r, current_func=state[ParseStateParseTree.key()].get_current_node_func(): current_func(r).get_complex_list()[-1])
                super()._do_parse(pstro, state, gen_args)

        return SymbolRule(**mself.__kwargs)

    def _new_levelstate(self, **kwargs):
        return MdlTypeParseRuleComplex.LevelState(**kwargs)

    class LevelState(Parser.ParseStateLevelStack.LevelState):
        def __init__(self, **kwargs):
            self._parent = kwargs["parent"]
            self._rule_order = []
            super().__init__(**kwargs)

            self._i = 0

        def _fixup_parserules(self, state):
            parserules = []
            if (self._i == len(self._parent._subrules)):
                self._i = 0
                parserules += [self._parent._endrule]

            parserules += list(self._special)
            parserules += self._parent._subrules[self._i]

            # Set parse rules
            state[Parser.ParseStateRules.key()].value = parserules

        def parsing(self, state):
            if self._i == 0:
                state[ParseStateParseTree.key()].set_current_node_func(lambda r, current_func=self._old_func: current_func(r).type)

        def parsed(self, state, accepted):
            if accepted.rule is self._parent._endrule:
                self.end_this(state)
                return

            for rule in self._parent._subrules[self._i]:
                if accepted.rule is rule:
                    self._i += 1
                    break

            self._rule_order.append(accepted.rule)
            self._fixup_parserules(state)

        def start(self, state):
            self._special = state[ParseStateSpecialRules].all()
            self._old_rules = state[Parser.ParseStateRules.key()].value
            self._old_func = state[ParseStateParseTree.key()].get_current_node_func()

            state_parsetree = state[ParseStateParseTree.key()]
            state_parsetree.current_node.type = self._parent._nodetype()
            state_parsetree.set_current_node_func(lambda r, current_func=self._old_func: current_func(r).type)

            self._fixup_parserules(state)

        def end(self, state):
            state[Parser.ParseStateRules.key()].value = self._old_rules
            state[ParseStateParseTree.key()].set_current_node_func(self._old_func)

        def _copy(self, new):
            super()._copy(new)

            new._rule_order = list(self._rule_order)

            new._special = self._special
            new._old_rules = self._old_rules
            new._old_func = self._old_func

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        return super()._gen_levelargs(state, **kwargs)

    def _do_parse(self, pstro, state, gen_args):
        if not pstro.match(self._chars[0]):
            raise Exception("No Open Symbol")

class MdlTypeParseRuleStruct(MdlTypeParseRuleComplex):
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        kwargs["nodetype"] = TypeStruct
        kwargs["subnodetype"] = TypeStructElement
        kwargs["chars"] = "{}"
        super().__init__(**kwargs)

    def _seprule(mself):
        class SymbolRule(MdlParseRuleBase):
            mname=mself._name
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                _name = ("" if self.mname is None else self.mname) + "!Sep"
            def _do_parse(self, pstro, state, gen_args):
                if not pstro.match(':'):
                    raise Exception("No Sep Symbol")

        return SymbolRule(**mself.__kwargs)

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        self._subrules = [
            [self._name_rule()],
            [self._seprule()],
            [self._config.config["typerule"]]
        ]
        return super()._gen_levelargs(state, **kwargs)



class MdlTypeParseRuleFunc(MdlTypeParseRuleComplex):
    def __init__(self, **kwargs):
        kwargs["nodetype"] = TypeFunction
        kwargs["subnodetype"] = TypeFunctionArgument
        kwargs["chars"] = "()"
        super().__init__(**kwargs)

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        self._subrules = [
            [self._name_rule()],
            [self._config.config["typerule"]]
        ]
        return super()._gen_levelargs(state, **kwargs)

def main():
    import sys

    config = MdlParserConfig({
        "symbol_chars": string.ascii_letters + "_",
        "symbol_first_chars": string.ascii_letters + "_" + string.digits})

    specialrules = ParseStateSpecialRules(
        whitespace=ParseRuleNameMod("whitespace", ParseRuleWhitespace()),
        comment=ParseRuleNameMod("comment", ParseRuleFromTillEndOfLine(char="#")))

    typerules = [
        ('void', TypeNone),
        ('char', TypeChar),

        ('float32', TypeFloat32),
        ('float64', TypeFloat64),

        ('int8', TypeInt8),
        ('int16', TypeInt16),
        ('int32', TypeInt32),
        ('int64', TypeInt64),

        ('uint8', TypeUInt8),
        ('uint16', TypeUInt16),
        ('uint32', TypeUInt32),
        ('uint64', TypeUInt64),
    ]

    type_args = {
        'modrules': [ParseRuleNameMod("TypeMod[Pointer]", 
            MdlTypeParseRuleBase(**{'keyword': '*', 'nodetype': TypePointer}))],
        'typerules': 
            [ParseRuleNameMod("TypeBase[{}]".format(t[0]),
                MdlTypeParseRuleBase(**{
                    'keyword': t[0], 
                    'nodetype': lambda nt=t[1]: nt})) 
            for t in typerules]
            + [
                MdlTypeParseRuleStruct(config=config),
                MdlTypeParseRuleFunc(config=config)
            ],
        'config': config
    }

    rule_symbol = ParseRuleNameMod("Symbol", MdlParseSymbol(config=config))
    rule_type = ParseRuleNameMod("Type", MdlTypeLevelParseRule(**type_args))
    rule_eol = ParseRuleNameMod("EOL", ParseRuleChar(char=";"))
    config.config["typerule"] = rule_type

    rule_typedef = ParseRuleNameMod("KeyWord[Type]", MdlKeywordParseRule(
        keyword="type",
        node_type=TypeDeclaration,
        subrules=[
            [rule_symbol],
            [rule_type],
            [rule_eol],
        ]
        ))
    rule_variable = ParseRuleNameMod("KeyWord[Var]", MdlKeywordParseRule(
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
