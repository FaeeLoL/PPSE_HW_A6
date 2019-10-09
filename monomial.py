from config import DEBUG
from exceptions import IncompatibleException


class Monomial:
    def __init__(self, var: str, num: int):
        self.var = var
        self.num = num

    def __str__(self):
        if DEBUG:
            return f'{{num: {self.num}, var: {self.var}}}'
        else:
            if self.num == 1:
                return self.var
            elif self.num == -1:
                return f'-{self.var}'
            elif self.num == 0:
                return '0'
            return f'{self.num}{self.var}'

    def __add__(self, other):
        if self.var != other.var:
            raise IncompatibleException
        return Monomial(self.var, self.num + other.num)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if self.var != other.var:
            raise IncompatibleException
        return Monomial(self.var, self.num - other.num)

    def __isub__(self, other):
        return self.__sub__(other)
