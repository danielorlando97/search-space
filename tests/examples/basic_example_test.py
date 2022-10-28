from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.errors import InvalidSampler, UnSupportOpError
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class BasicExamples(TestCase):

    #################################################################
    #                                                               #
    #                     Main Test                                 #
    #                                                               #
    #################################################################

    def test_get_random_value(self):
        space = Domain[int](min=50, max=100) | (lambda x: x != 65)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v >= 50
            assert v <= 100
            assert v != 65


    def test_get_two_random_value(self):
        space = Domain[int](min=50, max=100) | (lambda x: x != 65)
        space2 = Domain[int] | (lambda x, y=space: x < y)

        @replay_function
        def ______():
            v, context = space.get_sample()
            vy, _ = space2.get_sample(context)
            assert vy < v


    def test_get_random_str_by_condition(self):
        space = Domain[bool]()
        space2 = Domain[str](options=[str(i) for i in range(100)]) | (
            lambda x, y=space: (y | (x == '1'), y & (x != '1'))
        )

        @replay_function
        def ______():
            bool_, context = space.get_sample()
            string, _ = space2.get_sample(context)
            
            if bool_:
                assert string != '1'
            else:
                assert string == '1'

    def test_invalid_get_random_str_by_condition(self):
        space = Domain[bool]()

        try:
            space2 = Domain[str](options=[str(i) for i in range(100)]) | (
                lambda x, y=space: (y | x == '1', (y & (x != '1')))
            )
            assert False
        except UnSupportOpError:
            pass
        """
        In Python '|' has more priority than '==' because the 
        cmp op is 'or'. So our DSL need the breaks for conditionals
        expressions 
        """

     

    def test_get_random_value_by_func(self):

        def factorial(x: int):
            result = 1
            for i in range(2, x + 1):
                result *= i

            return result

        Factorial = FunctionalConstraint(factorial)


        space = Domain[int](max=10)
        space2 = Domain[int] | (lambda x, y=space: x < Factorial(y))

        @replay_function
        def ______():
            v, context = space.get_sample()
            v1, _ = space2.get_sample(context)
            
            assert v1 < factorial(v)

    def test_get_even_value(self):
        def is_even(x: int):
            for i in range(2, x//2 + 1):
                if x % i == 0:
                    return False
            return True    

        IsEven = FunctionalConstraint(is_even)
        space = Domain[int](min=2, max=500) | (lambda x : IsEven(x))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            
            assert is_even(v)

    #################################################################
    #                                                               #
    #                     Other Versions                            #
    #                     - Change Types                            #
    #                     - Change Dims                             #
    #                     - Change Constraint                       #
    #                                                               #
    #                                                               #
    #                                                               #
    #                                                               #
    #                                                               #
    #################################################################