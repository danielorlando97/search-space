from search_space.spaces import FunctionalConstraint
from typing import List

__all__ = [
    "Factorial"
]


@FunctionalConstraint
def Sum(x: List[int]):
    return sum(x)


@FunctionalConstraint
def Map(x: List[int], function):
    return list(map(function, x))
