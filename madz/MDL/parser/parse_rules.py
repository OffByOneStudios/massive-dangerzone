import string
import sys
import traceback

from .abstract_bases import *
from .parser import *
from .states import *

class ParseRuleBase(IParseRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name = self.__repr__()

    def _new_levelstate(self, **kwargs):
        return Parser.ParseStateLevelStack.LevelState(**kwargs)

    def p_chars(self, pstro, state, chars, first_chars=None):
        if not (first_chars is None) \
            and not pstro.test_in(first_chars):
            raise Exception("Bad first character")
        pstro.match_all(chars)

    def _gen_levelargs(self, state, **kwargs):
        #kwargs["state"] = state
        return kwargs

    def _gen_result(self, pstro, state, result_args, **kwargs):
        return ParseResult(
            _str=pstro.parsed(),
            _state=state,
            _rule=self,
            **result_args)

    def _gen_valid(self, pstro, state, result_args=dict(), **kwargs):
        my_args = {
            '_valid': True,
        }

        level_args = self._gen_levelargs(state, **kwargs)
        if not (level_args == {}):
            my_args['_new_level'] = self._new_levelstate(**level_args)

        my_args.update(result_args)
        return self._gen_result(pstro, state,
            result_args=my_args,
            **kwargs)

    def _gen_error(self, pstro, state, result_args=dict(), **kwargs):
        my_args = {
                '_valid': False,
                '_error': kwargs.get('error', None),
            }
        my_args.update(result_args)
        return self._gen_result(pstro, state,
            result_args=my_args,
            **kwargs)

    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, self._chars)

    def try_parse(self, pstr, state):
        try:
            pstro = ParseString(pstr)
            state = state

            gen_args = dict()
            parse_res = self._do_parse(pstro, state, gen_args)

            if parse_res is None:
                return self._gen_valid(pstro, state, **gen_args)
        except Exception as e:
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #print("ERROR: ",)
            #traceback.print_exception(exc_type, exc_value, exc_traceback, limit=8, file=sys.stdout)
            #print()
            return self._gen_error(pstro, state, error=e, **gen_args)
        return self._gen_error(pstro, state, error=parse_res, **gen_args)

    def __str__(self):
        return self._name


class ParseRuleChar(ParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._char = kwargs["char"]

    def _do_parse(self, pstro, state, gen_args):
        if (pstro.cur != self._char):
            raise Exception("Invalid char.")
        pstro.p()


class ParseRuleMatch(ParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._match = kwargs["match"]

    def _do_parse(self, pstro, state, gen_args):
        if not pstro.match(self._match):
            return "Invalid match."


class ParseRuleWhitespace(ParseRuleBase):
    def __init__(self, whitespace=string.whitespace, **kwargs):
        super().__init__(**kwargs)
        self._whitespace = whitespace

    def _do_parse(self, pstro, state, gen_args):
        self.p_chars(pstro, state, self._whitespace)
        if len(pstro.parsed()) == 0:
            return "Whitespace must have more than 0 charaters."


class ParseRuleFromTillEndOfLine(ParseRuleChar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._eol = kwargs.get("eol", '\n')

    def _do_parse(self, pstro, state, gen_args):
        sup = super()._do_parse(pstro, state, gen_args)
        if not (sup is None): return sup
        while(pstro.cur != None and pstro.cur != '\n'): pstro.p()


class ParseRuleLevelBase(ParseRuleBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _copy_level(self, new, old):
        new.accepted_rule_order = list(old.accepted_rule_order)

        new.init_state = old.init_state

    def _end_level(self, level, state):
        state[Parser.ParseStateRules.key()].value = level.init_state[Parser.ParseStateRules.key()].value
        state[ParseStateParseTree.key()].set_current_node_func(level.init_state[ParseStateParseTree.key()].get_current_node_func())

    def _init_level(self, level, state):
        pass

    def _generate_base_parserules(self, level, state):
        return list(level.init_state[ParseStateSpecialRules].all())

    def _update_level(self, level, state, accepted):
        pass

    class LevelState(Parser.ParseStateLevelStack.LevelState):
        def __init__(self, **kwargs):
            self._parent = kwargs["parent"]
            self.accepted_rule_order = []

            super().__init__(**kwargs)

        def set_parse_rules(self, state, rules):
            state[Parser.ParseStateRules.key()].value = rules

        def parsing(self, state):
            super().parsing(state)
            
            self._parent._update_level(self, state, None)

        def parsed(self, state, accepted):
            super().parsed(state, accepted)
            self.accepted_rule_order.append(accepted.rule)

            self._parent._update_level(self, state, accepted)

        def start(self, state):
            self.init_state = IParseState.copy_state(state)
            super().start(state)

            self._parent._init_level(self, state)

        def end(self, state):
            super().end(state)
            self._parent._end_level(self, state)

        def _copy(self, new):
            super()._copy(new)
            self.parent._copy_level(new, old)

    def _new_levelstate(self, **kwargs):
        return ParseRuleLevelBase.LevelState(**kwargs)

    def _gen_levelargs(self, state, **kwargs):
        kwargs["parent"] = self
        return super()._gen_levelargs(state, **kwargs)


def ParseRuleNameMod(name, base):
    base._name = name

    return base
