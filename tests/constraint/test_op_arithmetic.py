from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class ArithmeticConstraintOp(TestCase):
    def test_sum(self):
        space = Domain[int]() | (lambda x: x + 3 == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v + 3 == 10

    def test_sum_inverted(self):
        space = Domain[int]() | (lambda x: 3 + x == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v + 3 == 10

    def test_rest(self):
        space = Domain[int]() | (lambda x: x - 3 == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v - 3 == 10

    def test_rest_inverted(self):
        space = Domain[int]() | (lambda x: 30 - x == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert 30 - v == 10

    def test_mul(self):
        space = Domain[int]() | (lambda x: x * 3 == 30)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v * 3 == 30

    def test_mul_inverted(self):
        space = Domain[int]() | (lambda x: 3 * x == 30)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v * 3 == 30

    def test_div(self):
        space = Domain[int]() | (lambda x: x / 3 == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v / 3 == 10

    def test_div_inverted(self):
        space = Domain[int]() | (lambda x: 100 / x == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert 100 / v == 10
