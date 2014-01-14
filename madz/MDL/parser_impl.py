from .parser import *
from .nodes import *
from .base_types import *

class MdlParserConfig():
    def __init__(self, config):
        self.config = dict(config)
        # Expected types:
        #  symbol_chars
        #  symbol_first_chars
        #  typerule
        #  keyword_end


def MdlParseRuleBase(base=ParseRuleBase):
    class AMdlParseRuleBase(base):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._config = kwargs.get("config", MdlParserConfig({}))
    return AMdlParseRuleBase

class MdlKeywordParseRule(MdlParseRuleBase(ParseRuleLevelBase)):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._nodetype = kwargs["node_type"]
        self._keyword = kwargs["keyword"]
        self._subrules = [[self]] + kwargs["subrules"]

    def _copy_level(self, new, old):
        super()._copy_level(new, old)
        new._i = old._i

    def _init_level(self, level, state):
        super()._init_level(level, state)
        level._i = 1

    def _end_level(self, level, state):
        super()._end_level(level, state)
        state[ParseStateParseTree.key()].add_root()

    def _update_level(self, level, state, accepted):
        super()._update_level(level, state, accepted)
        if accepted is None:
            return

        if accepted.rule in self._subrules[level._i]:
            level._i += 1
        if level._i == len(self._subrules):
            level.finish(state)
            return

        rules = self._generate_base_parserules(level, state)
        rules += self._subrules[level._i]
        level.set_parse_rules(state, rules)

    def _do_parse(self, pstro, state, gen_args):
        if not pstro.match(self._keyword, case_insensitive=True):
            raise Exception("No Keyword")

        state[ParseStateParseTree.key()].current_root = self._nodetype()


class MdlParseSymbol(MdlParseRuleBase()):
    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, self._config.config["symbol_chars"], self._config.config["symbol_first_chars"])

        res = pstro.parsed()
        if len(res) == 0:
            raise Exception("Symbol must have more than 0 charaters.")

        state[ParseStateParseTree.key()].current_node.name = res


class MdlTypeParseRuleNamed(MdlParseRuleBase()):
    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, self._config.config["symbol_chars"] + ".", self._config.config["symbol_first_chars"])

        res = pstro.parsed()
        if len(res) == 0:
            raise Exception("Symbol must have more than 0 charaters.")

        state[ParseStateParseTree.key()].current_node.type = NamedType(res)


class MdlTypeLevelParseRule(MdlParseRuleBase(ParseRuleLevelBase)):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._modrules = kwargs["modrules"]
        self._typerules = kwargs["typerules"]

    def _end_level(self, level, state):
        state[Parser.ParseStateRules.key()].value = level.init_state[Parser.ParseStateRules.key()].value
        pass

    def _init_level(self, level, state):
        super()._init_level(level, state)
        rules = self._generate_base_parserules(level, state)
        rules += self._modrules
        rules += self._typerules

        level.set_parse_rules(state, rules)

    def _update_level(self, level, state, accepted):
        super()._update_level(level, state, accepted)
        if accepted is None:
            return

        if accepted.rule in self._typerules:
            level.finish(state)
            return

    def _do_parse(self, pstro, state, gen_args):
        pass


class MdlTypeParseRuleBase(MdlParseRuleBase()):
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


class MdlTypeParseRuleComplex(MdlParseRuleBase(ParseRuleLevelBase)):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__kwargs = kwargs
        self._chars = kwargs["chars"]
        self._nodetype = kwargs["nodetype"]
        self._subnodetype = kwargs["subnodetype"]

    def _end_rule(self):
        if not hasattr(self, "_endrule"):
            kwargs = dict(self.__kwargs)
            kwargs["match"] = self._chars[1]

            self._endrule = ParseRuleNameMod(
                ("" if self._name is None else self._name) + "!End",
                ParseRuleMatch(**kwargs))
        return self._endrule

    def _name_rule(mself):
        class SymbolRule(MdlParseSymbol):
            msubtype = mself._subnodetype
            mname=mself._name
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self._name = ("" if self.mname is None else self.mname) + "!Symbol"
            def _do_parse(self, pstro, state, gen_args):
                state[ParseStateParseTree.key()].current_node.get_complex_list().append(mself._subnodetype())
                state[ParseStateParseTree.key()].set_current_node_func(
                    lambda r, current_func=state[ParseStateParseTree.key()].get_current_node_func(): current_func(r).get_complex_list()[-1])
                super()._do_parse(pstro, state, gen_args)
        return SymbolRule(**mself.__kwargs)

    def _copy_level(self, new, old):
        super()._copy_level(new, old)
        new._i = old._i

    def _init_level(self, level, state):
        super()._init_level(level, state)
        level._i = 0
        
        state[ParseStateParseTree.key()].current_node.type = self._nodetype()

        old_func = level.init_state[ParseStateParseTree.key()].get_current_node_func()
        state[ParseStateParseTree.key()].set_current_node_func(
            lambda r, current_func=old_func: current_func(r).type)

        rules = self._generate_base_parserules(level, state)
        rules += [self._end_rule()]
        rules += self._subrules[level._i]
        level.set_parse_rules(state, rules)

    def _update_level(self, level, state, accepted):
        super()._update_level(level, state, accepted)
        if accepted is None:
            if level._i == 0:
                old_func = level.init_state[ParseStateParseTree.key()].get_current_node_func()
                state[ParseStateParseTree.key()].set_current_node_func(
                    lambda r, current_func=old_func: current_func(r).type)
            return

        if accepted.rule is self._end_rule():
            level.finish(state)
            return

        if accepted.rule in self._subrules[level._i]:
            level._i += 1
            if level._i == len(self._subrules):
                level._i = 0

        rules = self._generate_base_parserules(level, state)

        if (level._i == 0):
            rules += [self._end_rule()]

        rules += self._subrules[level._i]
        level.set_parse_rules(state, rules)

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

    def _seprule(self):
        kwargs = dict(self.__kwargs)
        kwargs["match"] = ":"

        return ParseRuleNameMod(
            ("" if self._name is None else self._name) + "!Sep",
            ParseRuleMatch(**kwargs))

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
        self.__kwargs = kwargs
        kwargs["nodetype"] = TypeFunction
        kwargs["subnodetype"] = TypeFunctionArgument
        kwargs["chars"] = "()"
        super().__init__(**kwargs)

    def _update_level(self, level, state, accepted):
        if not (accepted is None) and accepted.rule is self._end_rule():
            level._j = 0
            old_func = level.init_state[ParseStateParseTree.key()].get_current_node_func()
            state[ParseStateParseTree.key()].set_current_node_func(
                lambda r, current_func=old_func: current_func(r).type)
        if hasattr(level, '_j'):
            if accepted is None:
                if level._j == len(self._endrules):
                    level.finish(state)
                return
            if accepted.rule in self._endrules[level._j]:
                level._j += 1
            if level._j == len(self._endrules):
                return

            rules = self._generate_base_parserules(level, state)

            rules += self._endrules[level._j]
            level.set_parse_rules(state, rules)
            return
        super()._update_level(level, state, accepted)

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        self._subrules = [
            [self._name_rule()],
            [self._config.config["typerule"]]
        ]
        kwargs = dict(self.__kwargs)
        kwargs["match"] = "->"
        self._endrules = [
            [ParseRuleNameMod(
                ("" if self._name is None else self._name) + "!Arrow",
                ParseRuleMatch(**kwargs))],
            [self._config.config["typerule"]]
        ]
        return super()._gen_levelargs(state, **kwargs)


def generate_parser():
    config = MdlParserConfig({
        "symbol_chars": string.ascii_letters + "_" + string.digits, 
        "symbol_first_chars": string.ascii_letters + "_" })

    specialrules = ParseStateSpecialRules(
        whitespace=ParseRuleNameMod("whitespace", ParseRuleWhitespace(whitespace=string.whitespace + ',')),
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
                ParseRuleNameMod("TypeComplex[Struct]", MdlTypeParseRuleStruct(config=config)),
                ParseRuleNameMod("TypeComplex[Func]", MdlTypeParseRuleFunc(config=config)),
                ParseRuleNameMod("TypeComplex[Named]", MdlTypeParseRuleNamed(config=config))
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

    return parser


def get_result(parse):
    return parse[ParseStateParseTree.key()].roots


def main():
    import sys

    parser = generate_parser()

    rstate = parser.parse(open(sys.argv[1], 'r').read())

    print(rstate[Parser.ParseStateDebugStack.key()])
    print(rstate[ParseStateParseTree.key()])
