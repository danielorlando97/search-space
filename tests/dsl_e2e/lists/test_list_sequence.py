from typing import List
from unittest import TestCase

from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class SequencesList(TestCase):
    def test_asc(self):
        space = Domain[int][10]() | (lambda x, i: x[i-1] < x[i])

        @replay_function
        def ______():
            values, _ = space.get_sample()

            for i in range(1, len(values)):
                assert values[i-1] < values[i], values

    def test_asc_i_plus(self):
        space = Domain[int][10]() | (lambda x, i: x[i] < x[i + 1])

        @replay_function
        def ______():
            values, _ = space.get_sample()

            for i in range(1, len(values)):
                assert values[i-1] < values[i]

    def test_desc(self):
        space = Domain[int][10]() | (lambda x, i: x[i-1] > x[i])

        @replay_function
        def ______():
            values, _ = space.get_sample()

            for i in range(1, len(values)):
                assert values[i-1] > values[i]

    def test_desc_i_plus(self):
        space = Domain[int][10]() | (lambda x, i: x[i] > x[i + 1])

        @replay_function
        def ______():
            values, _ = space.get_sample()

            for i in range(1, len(values)):
                assert values[i-1] > values[i]

    def test_algebra(self):
        space = Domain[int][10]() | (lambda x, i: x[i-1] * 2 == x[i])

        @replay_function
        def ______():
            values, _ = space.get_sample()

            for i in range(1, len(values)):
                assert values[i-1] * 2 == values[i]

    def test_set(self):
        space = Domain[int][100]() | (lambda x, i: x[0: i] != x[i])

        @replay_function
        def ______():
            values, _ = space.get_sample()

            assert len(values) == len(set(values))
