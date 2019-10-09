from token import Token, parse_type, TokenType, Monomial
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
    def split_expr(expr: str) -> list:
        pre_tokens = expr.split(' ')
        results = list()
        for token in pre_tokens:
            if token.startswith('('):
                results.append(Token('('))
                if token.endswith(')'):
                    results.append(Token(token[1:-1]))
                    results.append(Token(')'))
                    continue
                results.append(Token(token[1:]))
            elif token.endswith(')'):
                results.append(Token(token[:-1]))
                results.append(Token(')'))
            else:
                found = False
                for i in range(len(token)):
                    try:
                        if parse_type(token[:i]) is TokenType.symbol and \
                                parse_type(token[i:]) is TokenType.number:
                            results.append(Token(token[:i]))
                            results.append(Token('*'))
                            results.append(Token(token[i:]))
                            found = True
                        elif parse_type(token[:i]) is TokenType.number and \
                                parse_type(token[i:]) is TokenType.symbol:
                            results.append(Token(token[i:]))
                            results.append(Token('*'))
                            results.append(Token(token[:i]))
                            found = True
                    except InvalidTypeException:
                        continue
                if found:
                    continue
                results.append(Token(token))
        return results

    def load_results(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].ttype is TokenType.results:
                self.tokens = self.tokens[:i] + helpers.history[
                    self.tokens[i].value].result + self.tokens[i + 1:]
            i += 1

    def __init__(self, expr: str) -> None:
        self.tokens = self.split_expr(expr)
        self.load_results()
        self.shunting_yard()
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
                            st.append(x)
                        elif ex.value == '-':
                            # x.value -= y.value
                            x -= y
                            st.append(x)
                        elif ex.value == '*':
                            if x.ttype is TokenType.symbol and \
                                    y.ttype is TokenType.number:
                                x.value = Monomial(x.value, y.value)
                                x.ttype = TokenType.monomial
                                st.append(x)
                        else:
                            raise YaDaunException
                    except IncompatibleException:
                        st.append(x)
                        st.append(y)
                        st.append(ex)
                except IndexError:
                    raise YaDaunException
        self.result = st

    def expand(self):
        pass

    def __str__(self):
        if DEBUG:
            return '[' + ', '.join(
                str(i) for i in self.tokens) + ']\n[' + ', '.join(
                str(i) for i in self.expr) + ']\n[' + ', '.join(
                str(i) for i in self.result) + ']'
        else:
            return str(self.result[0].value)
