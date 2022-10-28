from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class CustomSpace:
    ADomain = Domain[int]()
    BDomain = Domain[int]()
    CDomain = Domain[float]()
    DDomain = Domain[int][10]()

    def __init__(
        self,
        a: int = ADomain,
        b: int = BDomain,
        c: float = CDomain,
        d: List[int] = DDomain
    ) -> None:
        self.a, self.b = a, b
        self.c, self.d = c, d


class CustomConstraint(TestCase):
    def test_eq(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain == 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a == 10

    def test_neq(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain != 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a != 10

    def test_gl(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain > 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a > 10

    def test_gl_eq(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain >= 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a >= 10

    def test_le(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain < 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a < 10

    def test_le_eq(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain <= 10)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a <= 10

    def test_simple_or(self):
        space = Domain[CustomSpace]() | (lambda x: False | (x.ADomain < 10))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a < 10

    def test_simple_and(self):

        space = Domain[CustomSpace]() | (lambda x: True & (x.ADomain <= 10))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a <= 10

    def test_or(self):
        space = Domain[CustomSpace]() | (
            lambda x: (x.ADomain > 15) | (x.BDomain < 5))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b < 5 or v.a > 15

    def test_module(self):

        space = Domain[CustomSpace]() | (lambda x: x.ADomain % 3 == 2)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a % 3 == 2


class CustomConstraintByList(TestCase):
    def test_eq(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain == [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b in [10, 11, 12, 13]

    def test_neq(self):

        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain != [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert not v.b in [10, 11, 12, 13]

    def test_gl(self):

        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain > [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b > 13

    def test_gl_eq(self):

        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain >= [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b >= 13

    def test_le(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain < [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b < 10

    def test_le_eq(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain <= [10, 11, 12, 13])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b <= 10

    def test_module(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.BDomain % 3 == [1, 2])

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.b % 3 == 2 or v.b % 3 == 1


class CircularExternalDependency(TestCase):
    def test_eq(self):
        space = Domain[CustomSpace]() | (lambda x: x.ADomain == x.BDomain)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a == v.b

    def test_neq(self):

        space = Domain[CustomSpace]() | (lambda x: x.ADomain != x.BDomain)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a != v.b

    def test_gl(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.ADomain > x.BDomain + x.CDomain)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a > v.b + v.c

    def test_gl_eq(self):

        space = Domain[CustomSpace]() | (
            lambda x: x.ADomain >= x.BDomain * x.CDomain)

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a >= v.b * v.c

    def test_or(self):
        space = Domain[CustomSpace]() | (
            lambda x: (x.ADomain > x.BDomain) | (x.BDomain < x.ADomain))

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a > v.b or v.b > v.a

    def test_module(self):
        space = Domain[CustomSpace]() | (
            lambda x: (
                x.ADomain % x.BDomain == [1, 2],
                1 < x.BDomain, x.BDomain < 100,
                -1000 < x.ADomain, x.ADomain < 1000
            )
        )

        @replay_function
        def ______():
            v, _ = space.get_sample()
            assert v.a % v.b == 2 or v.a % v.b == 1

    def test_list(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.ADomain < x.DDomain)

        @replay_function
        def ______():
            v, _ = space.get_sample()

            for item in v.d:
                assert item > v.a

    def test_list_reversed(self):
        space = Domain[CustomSpace]() | (
            lambda x: x.ADomain < x.DDomain[3])

        @replay_function
        def ______():
            v, _ = space.get_sample()

            assert v.a < v.d[3]
