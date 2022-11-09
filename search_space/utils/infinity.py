# -*- coding: utf8 -*-

__author__ = 'Suilan Estévez Velarde'


INFINITY_MAX_VALUE = 100000000000000000000
INFINITY_MIN_VALUE = - 100000000000000000000


class Infinity:
    """Un valor mayor que todos los valores posibles
    de int() para comparaciones en el minimax
    """

    def __init__(self, positive=True):
        self.positive = positive

    def __le__(self, other):
        return not self.positive

    def __ge__(self, other):
        return self.positive

    def __lt__(self, other):
        return not self.positive

    def __gt__(self, other):
        return self.positive

    def __eq__(self, other):
        return False

    def __neg__(self):
        return Infinity(not self.positive)

    def __nonzero__(self):
        return True

    def __float__(self):
        if self.positive:
            return float(INFINITY_MAX_VALUE)

        return float(INFINITY_MIN_VALUE)

    def __add__(self, other):
        return self

    def __radd__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __rsub__(self, other):
        return -self

    def __mul__(self, other):
        if other == 0:
            return 0

        if other < 0:
            return -self

        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if other == 0:
            raise "Can't divide for zero"

        if other < 0:
            return -self

        return self

    def __rtruediv__(self, other):
        return 0

    def __str__(self) -> str:
        if self.positive:
            return 'oo'

        return '-oo'

    def __repr__(self) -> str:
        return self.__str__()

    def __abs__(self):
        if self.positive:
            return float(INFINITY_MAX_VALUE)

        return float(INFINITY_MIN_VALUE)


# Instancia global de infinito
oo = Infinity()
