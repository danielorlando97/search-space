from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class DynamicList(TestCase):
    def test(self):
        len_space = Domain[int](min=5, max=20)
        space = Domain[int][len_space]()

        @replay_function
        def ______():
            values, context = space.get_sample()
            l, context = space.get_sample(context=context)

            assert len(values) == l

    def test_matrix(self):
        len_space = Domain[int](min=5, max=20)
        space = Domain[int][len_space][len_space]()

        @replay_function
        def ______():
            values, context = space.get_sample()
            l, context = space.get_sample(context=context)

            assert len(values) == l

            for row in values:
                assert len(row) == l
