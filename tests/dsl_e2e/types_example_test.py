from unittest import TestCase
from search_space.dsl import Domain
from tests.config import replay_function


class TypesSpace(TestCase):

    #################################################################
    #                                                               #
    #                     Basic Types                               #
    #                                                               #
    #################################################################

    def test_int(self):
        N = Domain[int]()

        def test():
            value, _ = N.get_sample()
            assert type(value) == int

        replay_function(test)

    def test_float(self):
        R = Domain[float]()

        def test():
            value, _ = R.get_sample()
            assert type(value) == float

        replay_function(test)

    def test_bool(self):
        Space = Domain[bool]()

        def test():
            value, _ = Space.get_sample()
            assert type(value) == bool

        replay_function(test)

    def test_str(self):
        Space = Domain[str](options=[str(i) for i in range(100)])

        def test():
            value, _ = Space.get_sample()
            assert type(value) == str

        replay_function(test)

    #################################################################
    #                                                               #
    #                     List Types                                #
    #                                                               #
    #################################################################

    def test_list_int(self):
        N = Domain[int][10]()

        def test():
            value, _ = N.get_sample()

            for v in value:
                assert type(v) == int

        replay_function(test)

    def test_list_float(self):
        R = Domain[float][2][2]()

        def test():
            value, _ = R.get_sample()

            for row in value:
                for v in row:
                    assert type(v) == float

        replay_function(test)

    def test_list_bool(self):
        Space = Domain[bool][2][3][4]()

        def test():
            value, _ = Space.get_sample()

            for matrix in value:
                for row in matrix:
                    for v in row:
                        assert type(v) == bool

        replay_function(test)

    def test_list_str(self):
        Space = Domain[str][1][2][3][4](options=[str(i) for i in range(100)])

        def test():
            value, _ = Space.get_sample()

            for matrix in value[0]:
                for row in matrix:
                    for v in row:
                        assert type(v) == str

        replay_function(test)

    #################################################################
    #                                                               #
    #                     Custom Types                              #
    #                                                               #
    #################################################################

    def test_custom(self):
        class A:
            def __init__(self, a: int = Domain[int]()) -> None:
                self.a = a

        Space = Domain[A]()

        def test():
            value, _ = Space.get_sample()

            assert type(value) == A
            assert type(value.a) == int

        replay_function(test)

    def test_list_custom(self):
        class A:
            def __init__(self, a: int = Domain[int]()) -> None:
                self.a = a

        Space = Domain[A][10]()

        def test():
            value, _ = Space.get_sample()

            for v in value:
                assert type(v) == A
                assert type(v.a) == int

        replay_function(test)
