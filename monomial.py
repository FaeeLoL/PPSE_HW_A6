from config import DEBUG
from exceptions import IncompatibleException
import math


def stupid_multiplication_of_ints(a, b):
    m = (a < 0) ^ (b < 0)
    res = 0
    a, b = abs(a), abs(b)
    for i in range(b):
        res += a
    return -res if m else res


def stupid_division_of_ints(a, b):
    m = (a < 0) ^ (b < 0)
    res = 0
    a, b = abs(a), abs(b)
    while a >= b:
        res += 1
        a -= b
    return -res if m else res


def gcd(x, y):
    x = abs(x)
    y = abs(y)
    return math.gcd(x, y)


def lcm(x, y):
    return stupid_division_of_ints(stupid_multiplication_of_ints(x, y),
                                   gcd(x, y))


class Numbers:
    def __init__(self, num, den=1):
        self.num = num
        self.den = den
        self.__optimize()

    def __optimize(self):
        if self.den < 0:  # keep minus on numerator only
            self.num, self.den = -self.num, -self.den
        d = gcd(self.num, self.den)
        self.num = stupid_division_of_ints(self.num, d)
        self.den = stupid_division_of_ints(self.den, d)

    def __str__(self):
        if DEBUG:
            return f'{{num: {self.num}, den: {self.den}}}'
        if self.den == 1:
            return f'{self.num}'
        if self.den == 0:
            raise ZeroDivisionError
        if self.num == 0:
            return '0'
        return f'{self.num}/{self.den}'

    def __iadd__(self, other):
        self.__optimize()
        other.__optimize()
        d = lcm(self.den, other.den)
        self.num = stupid_multiplication_of_ints(
            self.num,
            stupid_division_of_ints(d, self.den),
        )
        self.den = d
        other.num = stupid_multiplication_of_ints(
            other.num,
            stupid_division_of_ints(d, other.den),
        )
        self.num += other.num
        self.__optimize()
        return self

    def __isub__(self, other):
        self.__optimize()
        other.__optimize()
        d = lcm(self.den, other.den)
        self.num = stupid_multiplication_of_ints(
            self.num,
            stupid_division_of_ints(d, self.den),
        )
        self.den = d
        other.num = stupid_multiplication_of_ints(
            other.num,
            stupid_division_of_ints(d, other.den),
        )
        self.num -= other.num
        self.__optimize()
        return self

    def __imul__(self, other):
        self.__optimize()
        other.__optimize()
        self.num = stupid_multiplication_of_ints(self.num, other.num)
        self.den = stupid_multiplication_of_ints(self.den, other.den)
        self.__optimize()
        return self

    def __itruediv__(self, other):
        self.__imul__(Numbers(other.den, other.num))
        return self


class Variables:
    def __init__(self, var):
        self.vars = dict()
        for i in var:
            if i in self.vars:
                self.vars[i] += 1
            else:
                self.vars[i] = 1

    def __clean_zeros(self):
        to_del = list()
        for k, v in self.vars.items():
            if v == 0:
                to_del.append(k)
        for i in to_del:
            del self.vars[i]

    def __eq__(self, other):
        self.__clean_zeros()
        other.__clean_zeros()
        if len(self.vars) != len(other.vars):
            return False
        for k, v in self.vars.items():
            if k not in other.vars or other.vars[k] != v:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __imul__(self, other):
        self.__clean_zeros()
        other.__clean_zeros()
        for k, v in other.vars.items():
            if k in self.vars:
                self.vars[k] += v
            else:
                self.vars[k] = v
        return self

    def __itruediv__(self, other):
        self.__clean_zeros()
        other.__clean_zeros()
        for k, v in other.vars.items():
            if k in self.vars:
                self.vars[k] -= v
            else:
                self.vars[k] = -v
        return self

    def __str__(self):
        if DEBUG:
            return self.vars.__str__()
        else:
            res = ''
            for k, v in self.vars.items():
                if v == 0:
                    continue
                if v == 1:
                    res += k
                    continue
                res += f'{k}^{v}'
            return res


class Monomial:
    def __init__(self, var: Variables, num: Numbers):
        self.var = var
        self.num = num

    def __str__(self):
        if DEBUG:
            return f'{{num: {self.num}, var: {self.var.__str__()}}}'
        else:
            if self.num.__str__() == '1':
                return self.var.__str__() or '1'
            if self.num.__str__() == '-1':
                return f'-{self.var.__str__()}' or '-1'
            elif self.num.__str__() == 0:
                return '0'
            return f'{self.num}{self.var.__str__()}'

    def __iadd__(self, other):
        if self.var != other.var:
            raise IncompatibleException
        self.num += other.num
        return self

    def __isub__(self, other):
        if self.var != other.var:
            raise IncompatibleException
        self.num -= other.num
        return self

    def __imul__(self, other):
        self.num *= other.num
        self.var *= other.var
        return self

    def __itruediv__(self, other):
        self.num /= other.num
        self.var /= other.var
        return self
