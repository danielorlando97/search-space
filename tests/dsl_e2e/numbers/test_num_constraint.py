from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class NumeralConstraint(TestCase):
    def test_eq(self):
        space = Domain[int]() | (lambda x: x == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v == 10

    def test_neq(self):
        space = Domain[int](max=15) | (lambda x: x != 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v != 10

    def test_gl(self):
        space = Domain[int](max=15) | (lambda x: x > 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > 5

    def test_gl_eq(self):
        space = Domain[int](max=15) | (lambda x: x >= 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v >= 5

    def test_le(self):
        space = Domain[int](max=15) | (lambda x: x < 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 5

    def test_le_eq(self):
        space = Domain[int](max=15) | (lambda x: x <= 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= 5

    def test_simple_or(self):
        space = Domain[int] | (lambda x: False | x < 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 5

    def test_simple_and(self):
        space = Domain[int](max=15) | (lambda x: True & x <= 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= 5

    def test_or(self):
        space = Domain[int](max=20) | (lambda x: x > 15 | x < 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 5 or v > 15

    def test_module(self):
        space = Domain[int] | (lambda x: x % 3 == 2)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2


class NumeralConstraintByList(TestCase):
    def test_eq(self):
        space = Domain[int]() | (lambda x: x == [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v in [10, 11, 12, 13]

    def test_neq(self):
        space = Domain[int](max=15) | (lambda x: x != [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert not v in [10, 11, 12, 13]

    def test_gl(self):
        space = Domain[int](max=15) | (lambda x: x > [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > 13

    def test_gl_eq(self):
        space = Domain[int](max=15) | (lambda x: x >= [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v >= 13

    def test_le(self):
        space = Domain[int](max=15) | (lambda x: x < [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 10

    def test_le_eq(self):
        space = Domain[int](max=15) | (lambda x: x <= [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= 10

    def test_module(self):
        space = Domain[int] | (lambda x: x % 3 == [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2 or v % 3 == 1


class NumeralFloatConstraint(TestCase):
    def test_eq(self):
        space = Domain[float]() | (lambda x: x == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v == 10

    def test_neq(self):
        space = Domain[float](max=15) | (lambda x: x != 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v != 10

    def test_gl(self):
        space = Domain[float](max=15) | (lambda x: x > 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > 5

    def test_gl_eq(self):
        space = Domain[float](max=15) | (lambda x: x >= 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v >= 5

    def test_le(self):
        space = Domain[float](max=15) | (lambda x: x < 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 5

    def test_le_eq(self):
        space = Domain[float](max=15) | (lambda x: x <= 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= 5

    def test_simple_or(self):
        space = Domain[float] | (lambda x: False | x < 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 5

    def test_simple_and(self):
        space = Domain[float](max=15) | (lambda x: True & x <= 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= 5

    def test_or(self):
        space = Domain[float](max=20) | (lambda x: x > 15 | x < 5)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 5 or v > 15

    def test_module(self):
        space = Domain[float] | (lambda x: x % 3 == 2)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2


class NumeralFloatConstraintByList(TestCase):
    def test_eq(self):
        space = Domain[float]() | (lambda x: x == [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v in [10, 11, 12, 13]

    def test_neq(self):
        space = Domain[float](max=15) | (lambda x: x != [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert not v in [10, 11, 12, 13]

    def test_gl(self):
        space = Domain[float](max=15) | (lambda x: x > [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > 13

    def test_gl_eq(self):
        space = Domain[float](max=15) | (lambda x: x >= [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v >= 13

    def test_le(self):
        space = Domain[float](max=15) | (lambda x: x < [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < 10

    def test_le_eq(self):
        space = Domain[float](max=15) | (lambda x: x <= [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= 10

    def test_module(self):
        space = Domain[float] | (lambda x: x % 3 == [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2 or v % 3 == 1
