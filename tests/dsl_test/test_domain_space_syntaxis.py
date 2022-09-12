from typing import List
from search_space.dsl import Domain, RandomValue
from tests.config import replay_function


def test_minimal_natural():
    def f():
        n = Domain[int]()
        assert n % 1 == 0
        assert type(n) == type(int())

    replay_function(f)


def test_minimal_real():
    def f():
        n = Domain[float]()
        assert type(n) == type(float())

    replay_function(f)


def test_numeral_limit():
    def f():
        n = Domain[float](min=10, max=100)
        assert 10 <= n and n <= 100

    replay_function(f)


def test_numeral_choice():
    def f():
        n = Domain[float](min=10, max=100)
        assert 10 <= n and n <= 100

    replay_function(f)


def test_string_choice():
    def f():
        options = ["White", "Black", "Red"]
        n = Domain[str](options=options)
        assert n in options

    replay_function(f)


def test_numeral_constraint():
    def f():
        n = Domain[float](lambda x: (x != 15, x != 16), min=10, max=20)
        assert 10 <= n and n <= 20 and not n in [15, 16]

    replay_function(f)


def test_list_numeral():
    def f():
        n = Domain[float][10](min=10, max=100)
        assert len(n) == 10
        assert [v for v in n if 10 <= v and v <= 100] == n

    replay_function(f)


def test_list_numeral():
    def f():
        options = ["White", "Black", "Red"]
        n = Domain[str][10](options=options)
        assert len(n) == 10
        assert [v for v in n if 10 <= v and v <= 100] == n

    replay_function(f)


def test_matrix_numeral():
    def f():
        n = Domain[float][10][10](min=10, max=100)
        assert len(n) == 10
        for row in n:
            assert len(row) == 10
            for v in row:
                assert 10 <= v and v <= 100

    replay_function(f)


def test_final_syntax():

    class ItemOfBagProblem:
        def __init__(
                self,
                weight: float = Domain[float](),
                price: float = Domain[float](min=10, max=100)
        ) -> None:
            self.weight = weight
            self.price = price

    class BagProblem:
        WeightDomain = Domain[float](min=50, max=100)
        ItemsLenDomain = Domain[int](max=20)
        ItemsListDomain = Domain[ItemOfBagProblem][ItemsLenDomain]() | (
            lambda x, w, i: (w in BagProblem.WeightDomain, x[i].weight <= w)
        )

        def __init__(
            self,
            weight: float = WeightDomain,
            itemsList: List[ItemOfBagProblem] = ItemsListDomain
        ) -> None:
            self.weight = weight
            self.itemsList = itemsList

        FaceableSolutionDomain = Domain[int][ItemsLenDomain]() | (
            lambda x, w, items, i: (
                w in BagProblem.WeightDomain,
                items in BagProblem.ItemsListDomain,
                Sum(x[0:i-1] * Map(items[0:i-1], lambda x: x.weight)) <= w
            )
        )

        def check_solution(self, solution: List[int] = FaceableSolutionDomain):
            ws = [self.itemsList[i].weight *
                  unitsOfItem for i, unitsOfItem in solution]
            ps = [self.itemsList[i].price *
                  unitsOfItem for i, unitsOfItem in solution]

            assert ws <= self.weight

            return ps

    problem = RandomValue[BagProblem]()

    assert 50 <= problem.weight and problem.weight <= 100
    assert len(problem.itemsList) <= 20
    for item in problem.itemsList:
        assert item.weight <= problem.weight
