from token import Token, parse_type, TokenType
from monomial import Monomial, Variables, Numbers
from exceptions import *
from config import DEBUG
import copy
import helpers


def print_tokens_list(items):
    print('[' + ', '.join(str(i) for i in items) + ']')


class Expression:
    tokens = list
    expr = None
    result = None

    @staticmethod
    def __split_token(token: str) -> list:
        found = False
        results = []
        for i in range(len(token)):
            try:
                if token[i] == '/' and \
                        parse_type(token[:i]) is TokenType.number and \
                        parse_type(token[i + 1:]) is TokenType.number:
                    results.append(Token(
                        item=Monomial(Variables(''),
                                      Numbers(int(token[:i]),
                                              int(token[i + 1:])),
                                      ),
                        ttype=TokenType.monomial,
                    ))
                    found = True
            except InvalidTypeException:
                pass
            try:
                if parse_type(token[:i]) is TokenType.symbol and \
                        parse_type(token[i:]) is TokenType.number:
                    results.append(Token(
                        item=Monomial(Variables(token[:i]),
                                      Numbers(int(token[i:]))),
                        ttype=TokenType.monomial,
                    ))
                    found = True
                elif parse_type(token[:i]) is TokenType.number and \
                        parse_type(token[i:]) is TokenType.symbol:
                    results.append(Token(
                        item=Monomial(Variables(token[i:]),
                                      Numbers(int(token[:i]))),
                        ttype=TokenType.monomial,
                    ))
                    found = True
            except InvalidTypeException:
                continue
        if found:
            return results
        results.append(Token(token))
        return results

    @staticmethod
    def __split_expr(expr: str) -> list:
        pre_tokens = expr.split(' ')
        results = list()
        for token in pre_tokens:
            if token.startswith('('):
                results.append(Token('('))
                if token.endswith(')'):
                    results += Expression.__split_token(token[1:-1])
                    results.append(Token(')'))
                    continue
                results += Expression.__split_token(token[1:])
            elif token.endswith(')'):
                results += Expression.__split_token(token[:-1])
                results.append(Token(')'))
            else:
                results += Expression.__split_token(token)
        return results

    def load_results(self):
        i = 0
        while i < len(self.expr):
            if self.expr[i].ttype is TokenType.results:
                self.expr = self.expr[:i] + helpers.history[
                    self.expr[i].value].result + self.expr[i + 1:]
            i += 1

    def __init__(self, expr: str) -> None:
        self.tokens = Expression.__split_expr(expr)
        self.shunting_yard()
        self.load_results()
        self.calculate()

    def shunting_yard(self):
        res = list()
        st = list()
        for token in self.tokens:
            if token.ttype is TokenType.number:
                res.append(token)
            if token.ttype is TokenType.symbol:
                res.append(token)
            if token.ttype is TokenType.monomial:
                res.append(token)
            if token.ttype is TokenType.results:
                res.append(token)
            elif token.ttype is TokenType.operator:
                while len(st) != 0 and (st[-1].ttype is TokenType.operator or
                                        st[-1].ttype is TokenType.operator2):
                    res.append(st.pop())
                st.append(token)
            elif token.ttype is TokenType.operator2:
                while len(st) != 0 and st[-1].ttype is TokenType.operator2:
                    res.append(st.pop())
                st.append(token)
            elif token.ttype is TokenType.open_bracket:
                st.append(token)
            elif token.ttype is TokenType.close_bracket:
                while st[-1].ttype is not TokenType.open_bracket:
                    res.append(st.pop())
                    if len(st) == 0:
                        raise InvalidExpressionException
                st.pop()
        while len(st) != 0:
            if st[-1].ttype is TokenType.open_bracket:
                raise InvalidExpressionException
            elif st[-1].ttype is TokenType.operator or \
                    st[-1].ttype is TokenType.operator2:
                res.append(st.pop())
            else:
                raise YaDaunException

        self.expr = res

    def calculate(self):
        if DEBUG:
            print("CALCULATION")
        st = list()
        for ex in self.expr:
            if DEBUG:
                print_tokens_list(st)
            if ex.ttype is TokenType.number or \
                    ex.ttype is TokenType.symbol or \
                    ex.ttype is TokenType.monomial:
                st.append(ex)
            elif ex.ttype is TokenType.operator or \
                    ex.ttype is TokenType.operator2:
                try:
                    # use copy, because without breaks
                    # items in other lists
                    y = copy.copy(st.pop())
                    x = copy.copy(st.pop())
                    try:
                        if ex.value == '+':
                            x += y
                        elif ex.value == '-':
                            x -= y
                        elif ex.value == '*':
                            x *= y
                        elif ex.value == '/':
                            x /= y
                        else:
                            raise YaDaunException
                        st.append(x)
                    except IncompatibleException:
                        st.append(x)
                        st.append(y)
                        st.append(ex)
                except IndexError:
                    raise YaDaunException
        if DEBUG:
            print_tokens_list(st)
        self.result = st

    def expand(self):
        pass

    def to_infix(self):
        res = []
        for item in self.result:
            if item.ttype is TokenType.number or \
                    item.ttype is TokenType.monomial:
                res.insert(0, item.value.__str__())
            else:
                op1 = res.pop(0)
                op2 = res.pop(0)
                res.insert(0, f'({op2} {item.__str__()} {op1})')
        result = res[0]
        # Count correct bracket sequence to remove brackets
        # if they cover the whole expression
        if len(result) < 2:
            return result
        cnt = 0
        for i in result[:-1]:
            if i == '(':
                cnt += 1
            elif i == ')':
                cnt -= 1
            if cnt == 0:
                return result
        return result[1:-1]

    def __str__(self):
        if DEBUG:
            return '[' + ', '.join(
                str(i) for i in self.tokens) + ']\n[' + ', '.join(
                str(i) for i in self.expr) + ']\n[' + ', '.join(
                str(i) for i in self.result) + ']'
        else:
            return self.to_infix()
