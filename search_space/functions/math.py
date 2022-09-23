from search_space.spaces import FunctionalConstraint


__all__ = [
    "Factorial"
]


@FunctionalConstraint
def Factorial(x: int):
    result = 1
    for i in range(2, x + 1):
        result *= i

    return result
