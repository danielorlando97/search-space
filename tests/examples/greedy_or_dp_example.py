from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function

#################################################################
#                                                               #
#                BagProblem Test                                #
#                                                               #
#################################################################


class BagItem:
    WeightDomain = Domain[float]()
    PriceDomain = Domain[float](max=50)

    def __init__(self, w: float = WeightDomain, p: float = PriceDomain) -> None:
        self.w, self.p = w, p


class BagProblem:
    WeightDomain = Domain[float](max=100)
    ItemsLenDomain = Domain[int](min=5, max=20)
    ItemsDomain = Domain[BagItem][ItemsLenDomain] | (
        lambda x, i, w=WeightDomain: x[i].WeightDomain < w
    )

    def __init__(self, w: float = WeightDomain, items: List[BagItem] = ItemsDomain) -> None:
        self.w, self.items = w, items


# @FunctionalConstraint
# def ComputingCurrentCapacity(w: float, items: List[BagItem], i: int):
#     if i < 1:
#         return w
#     return (w - sum([item.w for item in items[:i]])) / items[i].w

@FunctionalConstraint
def ComputingCurrentCapacity(w: float, items: List[BagItem], current_counts: List[float]):
    current_w = sum([count * item.w for count,
                    item in zip(current_counts, items)])
    return (w - current_w) / items[len(current_counts)].w


class BagSolution(BagProblem):
    SolutionDomain = Domain[int][BagProblem.ItemsLenDomain] | (
        lambda x, i, w=BagProblem.WeightDomain, items=BagProblem.ItemsDomain: (
            x[i] < ComputingCurrentCapacity(w, items, x[:i - 1])
        )
    )

    def validate_solution(self, solution: List[int] = SolutionDomain):
        price = sum([item.p * count for item,
                     count in zip(self.items, solution)])
        weight = sum([item.w * count for item,
                     count in zip(self.items, solution)])
        assert self.w >= weight
        return price


class BagProblemTest(TestCase):

    def test(self):
        space = Domain[BagSolution]()

        @replay_function
        def ______():
            bag_problem_solution, _ = space.get_sample()

            for item in bag_problem_solution.items:
                assert item.w < bag_problem_solution.w

            @replay_function
            def ______():
                price = bag_problem_solution.validate_solution()
