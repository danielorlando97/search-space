from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function

options = [str(i) for i in range(100)]


class StringConstraint(TestCase):
    def test_eq(self):
        space = Domain[str](options=options) | (lambda x: x == '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v == '10'

    def test_neq(self):
        space = Domain[str](options=options) | (lambda x: x != '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v != '10'

    def test_gl(self):
        space = Domain[str](options=options) | (lambda x: x > '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > '10'

    def test_gl_eq(self):
        space = Domain[str](options=options) | (lambda x: x >= '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v >= '10'

    def test_le(self):
        space = Domain[str](options=options) | (lambda x: x < '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < '10'

    def test_le_eq(self):
        space = Domain[str](options=options) | (lambda x: x <= '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v <= '10'

    def test_simple_or(self):
        space = Domain[str](options=options) | (lambda x: False | x > '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > '10'

    def test_simple_and(self):
        space = Domain[str](options=options) | (lambda x: True & x > '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > '10'

    def test_or(self):
        space = Domain[str](options=options) | (lambda x: x < '100' | x > '10')

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < '100' or v > '10'


class StringConstraintByList(TestCase):
    def test_eq(self):
        space = Domain[str](options=options) | (
            lambda x: x == ["10", "11", "12", "13"]
        )

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v in ["10", "11", "12", "13"]

    def test_neq(self):
        space = Domain[str](options=options) | (
            lambda x: x != ["10", "11", "12", "13"]
        )

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert not v in ["10", "11", "12", "13"]

    def test_gl(self):
        space = Domain[str](options=options) | (
            lambda x: x > ["10", "11", "12", "13"]
        )

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v > "13"

    def test_le(self):
        space = Domain[str](options=options) | (
            lambda x: x > ["10", "11", "12", "13"]
        )

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v < "10"
