from search_space.spaces.functions_and_predicates import Function
from math import sqrt


class Sqrt(Function):
    def __invert__(self, x):
        return x ** 2

    def __call__(self, x):
        return sqrt(x)
