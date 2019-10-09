from enum import Enum

import helpers
from exceptions import InvalidTypeException, InvalidHistoryCallException, \
    IncompatibleException
from config import DEBUG


class TokenType(Enum):
    number = 1
    operator = 2
    open_bracket = 3
    close_bracket = 4
    results = 5
    symbol = 6
    operator2 = 7
    monomial = 8


class Monomial:
    def __init__(self, var: str, num: int):
        self.var = var
        self.num = num

    def __str__(self):
        if DEBUG:
            return f'{{num: {self.num}, var: {self.var}}}'
        else:
            return f'{self.num}{self.var}'

    def __add__(self, other):
        if self.var != other.var:
            raise IncompatibleException
        return Monomial(self.var, self.num + other.num)

    def __iadd__(self, other):
        self.__add__(other)

    def __sub__(self, other):
        if self.var != other.var:
            raise IncompatibleException
        return Monomial(self.var, self.num - other.num)

    def __isub__(self, other):
        self.__sub__(other)


def parse_type(item: str) -> TokenType:
    if item in ['+', '-']:
        return TokenType.operator
    elif item in ['*', '/']:
        return TokenType.operator2
    elif item == '(':
        return TokenType.open_bracket
    elif item == ')':
        return TokenType.close_bracket
    elif len(item) > 0 and item[0] == '[' and item[-1] == ']' and parse_type(
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
    def __init__(self, item: str, ttype=None):
        self.value = item
        if ttype is not None:
            self.ttype = ttype
            return
        self.ttype = parse_type(item)
        self.cast_value()

    def cast_value(self):
        if self.ttype is TokenType.number:
            self.value = int(self.value)
        elif self.ttype is TokenType.results:
            self.value = int(self.value[1:-1])
            if self.value >= len(helpers.history):
                raise InvalidHistoryCallException

    def __iadd__(self, other):
        if self.ttype is TokenType.number:
            if other.ttype is TokenType.number:
                self.value += other.value
                return self
            else:
                raise IncompatibleException
        elif self.ttype is TokenType.symbol:
            if other.ttype is TokenType.symbol:
                if self.value == other.value:
                    self.ttype = TokenType.monomial
                    self.value = Monomial(other.value, 2)
                    return self
                else:
                    raise IncompatibleException
            elif other.ttype is TokenType.monomial and \
                    self.value == other.value.var:
                other.value.num += 1
                return other
            else:
                raise IncompatibleException
        elif self.ttype is TokenType.monomial:
            if other.ttype is TokenType.monomial:
                self.value += other.value
                return self
            elif other.ttype is TokenType.symbol and \
                    self.value.var == other.value:
                self.value.num += 1
                return self
            else:
                raise IncompatibleException
        else:
            raise InvalidTypeException

    def __isub__(self, other):
        if self.ttype is TokenType.number:
            if other.ttype is TokenType.number:
                self.value -= other.value
                return self
            else:
                raise IncompatibleException
        elif self.ttype is TokenType.symbol:
            if other.ttype is TokenType.symbol:
                if self.value == other.value:
                    self.ttype = TokenType.number
                    self.value = 0
                    return self
                raise IncompatibleException
            elif other.ttype is TokenType.monomial and \
                    self.value == other.value.var:
                other.value.num = 1 - other.value.num
                return other
            else:
                raise IncompatibleException
        elif self.ttype is TokenType.monomial:
            if other.ttype is TokenType.monomial:
                self.value -= other.value
                return self
            elif other.ttype is TokenType.symbol and \
                    self.value.var == other.value:
                self.value.num -= 1
                return self
            else:
                raise IncompatibleException
        else:
            raise InvalidTypeException

    def __str__(self):
        if DEBUG:
            return f'{{{self.ttype.__str__()}, {self.value.__str__()}}}'
        else:
            return self.value.__str__()
