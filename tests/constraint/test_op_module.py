from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class ModularConstraintOp(TestCase):
    def test_eq(self):
        space = Domain[int]() | (lambda x: x % 3 == 2)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2

    def test_neq(self):
        space = Domain[int]() | (lambda x: x % 3 != 2)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 != 2

    def test_gl(self):
        space = Domain[int]() | (lambda x: x % 3 > 1)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 > 1

    def test_gl_eq(self):
        space = Domain[int]() | (lambda x: x % 3 >= 1)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 >= 1

    def test_le(self):
        space = Domain[int]() | (lambda x: x % 3 < 1)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 < 1

    def test_le_eq(self):
        space = Domain[int]() | (lambda x: x % 3 <= 1)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 <= 1

    def test_or(self):
        space = Domain[int](max=20) | (lambda x: (x % 3) | (x % 2))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 0 or v % 2 == 0

    def test_with_other(self):
        space = Domain[int](max=20) | (lambda x: (x % 3 == 2, x > 100))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2 and v > 100

    def test_with_other_plus(self):
        space = Domain[int](max=20) | (
            lambda x: (x % 3 == 2, x > 0, x < 10, x != 5))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 == 2 and v > 0 and v < 10 and v != 5


class ModularConstraintOp(TestCase):
    def test_eq(self):
        space = Domain[int]() | (lambda x: x % 3 == [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 in [1, 2]

    def test_neq(self):
        space = Domain[int]() | (lambda x: x % 3 != [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert not v % 3 in [1, 2]

    def test_gl(self):
        space = Domain[int]() | (lambda x: x % 3 > [0, 1])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 > 1

    def test_gl_eq(self):
        space = Domain[int]() | (lambda x: x % 3 >= [0, 1])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 >= 1

    def test_le(self):
        space = Domain[int]() | (lambda x: x % 3 < [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 < 1

    def test_le_eq(self):
        space = Domain[int]() | (lambda x: x % 3 <= [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v % 3 <= 1

    def test_with_other_plus(self):
        space = Domain[int](max=20) | (
            lambda x: (x % 3 == 2, x > 0, x < 10, x != [2, 5]))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v == 8
