from enum import Enum

import helpers
from config import DEBUG
from exceptions import InvalidTypeException, InvalidHistoryCallException, \
    IncompatibleException
from monomial import Monomial, Variables, Numbers


class TokenType(Enum):
    number = 1
    operator = 2
    open_bracket = 3
    close_bracket = 4
    results = 5
    symbol = 6
    operator2 = 7
    monomial = 8
    fraction = 9


def parse_type(item: str) -> TokenType:
    if item in ['+', '-']:
        return TokenType.operator
    elif item in ['*', '/']:
        return TokenType.operator2
    elif item == '(':
        return TokenType.open_bracket
    elif item == ')':
        return TokenType.close_bracket
    elif item == '[last]' or len(item) > 0 and item[0] == '[' and \
            item[-1] == ']' and parse_type(
        item[1:-1]) == TokenType.number:
        return TokenType.results
    elif item.isalpha():
        return TokenType.symbol
    else:
        try:
            int(item)
            return TokenType.number
        except ValueError:
            raise InvalidTypeException


class Token:
    def __init__(self, item, ttype=None):
        self.value = item
        if ttype is not None:
            self.ttype = ttype
            return
        self.ttype = parse_type(item)
        self.cast_value()

    def cast_value(self):
        if self.ttype is TokenType.number:
            self.value = Monomial(Variables(''), Numbers(int(self.value)))
            self.ttype = TokenType.monomial
        elif self.ttype is TokenType.results:
            if self.value == '[last]':
                if not helpers.history:
                    raise InvalidHistoryCallException
                self.value = len(helpers.history) - 1
                return
            self.value = int(self.value[1:-1])
            if self.value >= len(helpers.history):
                raise InvalidHistoryCallException
        elif self.ttype is TokenType.symbol:
            self.value = Monomial(Variables(self.value), Numbers(1))
            self.ttype = TokenType.monomial

    def __iadd__(self, other):
        if self.ttype is TokenType.number:
            if other.ttype is TokenType.number:
                self.value += other.value
                return self
        elif self.ttype is TokenType.monomial:
            if other.ttype is TokenType.monomial:
                self.value += other.value
                if self.value.num == 0:
                    self.value = 0
                    self.ttype = TokenType.number
                return self
        raise IncompatibleException

    def __isub__(self, other):
        if self.ttype is TokenType.number:
            if other.ttype is TokenType.number:
                self.value -= other.value
                return self
        elif self.ttype is TokenType.monomial:
            if other.ttype is TokenType.monomial:
                self.value -= other.value
                if self.value.num == 0:
                    self.value = 0
                    self.ttype = TokenType.number
                return self
        raise IncompatibleException

    def __imul__(self, other):
        if self.ttype is TokenType.monomial:
            if other.ttype is TokenType.monomial:
                self.value *= other.value
                if self.value.num == 0:
                    self.value.var.vars = dict()
                return self
        raise IncompatibleException

    def __itruediv__(self, other):
        if self.ttype is TokenType.monomial:
            if other.ttype is TokenType.monomial:
                self.value /= other.value
                if self.value.num == 0:
                    self.value.var.vars = dict()
                return self
        raise IncompatibleException

    def __str__(self):
        if DEBUG:
            return f'{{{self.ttype.__str__()}, {self.value.__str__()}}}'
        else:
            return self.value.__str__()
