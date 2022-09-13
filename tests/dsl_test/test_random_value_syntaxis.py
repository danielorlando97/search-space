from search_space.dsl import RandomValue
from tests.config import replay_function


def test_minimal_natural():
    def f():
        n = RandomValue[int]()
        assert n % 1 == 0
        assert type(n) == type(int())

    replay_function(f)


def test_minimal_real():
    def f():
        n = RandomValue[float]()
        assert type(n) == type(float())

    replay_function(f)


def test_numeral_limit():
    def f():
        n = RandomValue[float](min=10, max=100)
        assert 10 <= n and n <= 100

    replay_function(f)


def test_numeral_choice():
    def f():
        n = RandomValue[float](min=10, max=100)
        assert 10 <= n and n <= 100

    replay_function(f)


def test_string_choice():
    def f():
        options = ["White", "Black", "Red"]
        n = RandomValue[str](options=options)
        assert n in options

    replay_function(f)


def test_numeral_constraint():
    def f():
        n = RandomValue[float](lambda x: (x != 15, x != 16), min=10, max=20)
        assert 10 <= n and n <= 20 and not n in [15, 16]

    replay_function(f)


def test_list_numeral():
    def f():
        n = RandomValue[float][10](min=10, max=100)
        assert len(n) == 10
        assert [v for v in n if 10 <= v and v <= 100] == n

    replay_function(f)


def test_list_numeral():
    def f():
        options = ["White", "Black", "Red"]
        n = RandomValue[str][10](options=options)
        assert len(n) == 10
        assert [v for v in n if v in options] == n

    replay_function(f)


def test_matrix_numeral():
    def f():
        n = RandomValue[float][10][10](min=10, max=100)
        assert len(n) == 10
        for row in n:
            assert len(row) == 10
            for v in row:
                assert 10 <= v and v <= 100

    replay_function(f)
