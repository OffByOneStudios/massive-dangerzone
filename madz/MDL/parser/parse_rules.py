import string
import sys
import traceback

from .abstract_bases import *
from .parser import *

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
            return "Invalid char."
        pstro.p()

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

def ParseRuleNameMod(name, base):
    base._name = name

    return base
