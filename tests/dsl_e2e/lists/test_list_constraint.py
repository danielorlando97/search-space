from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class NumeralConstraint(TestCase):
    def test_eq(self):
        space = Domain[int][10]() | (lambda x, i: x[i] == 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v == 10

    def test_neq(self):
        space = Domain[int][10](min=9, max=11) | (lambda x, i: x[i] != 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v != 10

    def test_gl(self):
        space = Domain[int][10](max=15) | (lambda x, i: x[i] > 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v > 10

    def test_gl_eq(self):
        space = Domain[int][10](max=15) | (lambda x, i: x[i] >= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v >= 10

    def test_le(self):
        space = Domain[int][10]() | (lambda x, i: x[i] < 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v < 10

    def test_le_eq(self):
        space = Domain[int][10]() | (lambda x, i: x[i] <= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v <= 10

    def test_simple_or(self):
        space = Domain[int][10]() | (lambda x, i: False | x[i] <= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v <= 10

    def test_simple_and(self):
        space = Domain[int][10]() | (lambda x, i: True & x[i] <= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v <= 10

    def test_or(self):
        space = Domain[int][10]() | (lambda x, i: x[i] > 15 | x[i] < 5)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v < 5 or v > 15

    def test_module(self):
        space = Domain[int][10]() | (lambda x, i: x[i] % 3 == 2)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v % 3 == 2


class NumeralConstraintByList(TestCase):
    def test_eq(self):
        space = Domain[int][10]() | (lambda x, i: x[i] == [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v in [10, 11, 12, 13]

    def test_neq(self):
        space = Domain[int][10](max=15) | (
            lambda x, i: x[i] != [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert not v in [10, 11, 12, 13]

    def test_gl(self):
        space = Domain[int][10](max=15) | (
            lambda x, i: x[i] > [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v > 13

    def test_gl_eq(self):
        space = Domain[int][10](max=15) | (
            lambda x, i: x[i] >= [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v >= 13

    def test_le(self):
        space = Domain[int][10](max=15) | (
            lambda x, i: x[i] < [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v < 10

    def test_le_eq(self):
        space = Domain[int][10](max=15) | (
            lambda x, i: x[i] <= [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v <= 10

    def test_module(self):
        space = Domain[int][10] | (lambda x, i: x[i] % 3 == [1, 2])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for v in values:
                assert v % 3 == 2 or v % 3 == 1


class NumeralDim2Constraint(TestCase):
    def test_eq(self):
        space = Domain[int][10][10]() | (lambda x, i, j: x[i][j] == 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v == 10

    def test_neq(self):
        space = Domain[int][10][10](min=9, max=11) | (
            lambda x, i, j: x[i][j] != 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v != 10

    def test_gl(self):
        space = Domain[int][10][10](max=15) | (lambda x, i, j: x[i][j] > 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v > 10

    def test_gl_eq(self):
        space = Domain[int][10][10](max=15) | (lambda x, i, j: x[i][j] >= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v >= 10

    def test_le(self):
        space = Domain[int][10][10]() | (lambda x, i, j: x[i][j] < 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v < 10

    def test_le_eq(self):
        space = Domain[int][10][10]() | (lambda x, i, j: x[i][j] <= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v <= 10

    def test_simple_or(self):
        space = Domain[int][10][10]() | (lambda x, i, j: False | x[i][j] <= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v <= 10

    def test_simple_and(self):
        space = Domain[int][10][10]() | (lambda x, i, j: True & x[i][j] <= 10)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v <= 10

    def test_or(self):
        space = Domain[int][10][10]() | (
            lambda x, i, j: x[i][j] > 15 | x[i][j] < 5)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v < 5 or v > 15

    def test_module(self):
        space = Domain[int][10][10]() | (lambda x, i, j: x[i][j] % 3 == 2)

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v % 3 == 2


class NumeralConstraintByList(TestCase):
    def test_eq(self):
        space = Domain[int][10][10]() | (
            lambda x, i, j: x[i][j] == [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v in [10, 11, 12, 13]

    def test_neq(self):
        space = Domain[int][10][10](max=15) | (
            lambda x, i, j: x[i][j] != [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert not v in [10, 11, 12, 13]

    def test_gl(self):
        space = Domain[int][10][10](max=15) | (
            lambda x, i, j: x[i][j] > [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v > 13

    def test_gl_eq(self):
        space = Domain[int][10][10](max=15) | (
            lambda x, i, j: x[i][j] >= [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v >= 13

    def test_le(self):
        space = Domain[int][10][10](max=15) | (
            lambda x, i, j: x[i][j] < [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v < 10

    def test_le_eq(self):
        space = Domain[int][10][10](max=15) | (
            lambda x, i, j: x[i][j] <= [10, 11, 12, 13])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v <= 10

    def test_module(self):
        space = Domain[int][10][10] | (lambda x, i, j: x[i][j] % 3 == [1, 2])

        @replay_function
        def ______():
            values, _ = space.get_sample()
            for row in values:
                for v in row:
                    assert v % 3 == 2
