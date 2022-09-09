from search_space.spaces.functions_and_predicates import Function


class Factorial(Function):

    def __call__(self, x):
        result = 1

        for i in range(2, x + 1):
            result *= i

        return result
