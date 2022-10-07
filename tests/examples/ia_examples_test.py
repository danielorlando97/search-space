from typing import List
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function

#################################################################
#                                                               #
#                ColorMap Test                                  #
#                                                               #
#################################################################


@FunctionalConstraint
def AdjColors(_map: List[List[bool]], country_colored: List[int], color_len):
    index = len(country_colored)
    result = set()
    for i, is_adj_country in enumerate(_map[index]):
        if i < index and is_adj_country:
            result.add(country_colored[i])
    if len(result) == color_len:
        return []
        return list(result)


class ColorMapProblem:
    CountryLenDomain = Domain[int](max=20)
    ColorLenDomain = Domain[int](min=1) | (
        lambda x, cl=CountryLenDomain: x < cl)

    MapDomain = Domain[bool][CountryLenDomain][CountryLenDomain] | (
        lambda x, i, j: x[i][j] == x[j][i]
    )

    def __init__(self, color_len: int = ColorLenDomain, adj_map: List[List[bool]] = MapDomain) -> None:
        self.cl, self.map = color_len, adj_map

    SolutionDomain = Domain[int][CountryLenDomain] | (
        lambda x, i, color_len=ColorLenDomain, _map=MapDomain: (
            x[i] < color_len,
            x[i] != AdjColors(_map, x[0:i-1], color_len)
        )
    )

    def validate_solution(self, solution: List[int] = SolutionDomain):
        assert len(solution) == len(self.map)

        for color in solution:
            assert color < self.cl

        for i, row in enumerate(self.map):
            for j, are_adj in enumerate(row):
                if are_adj and solution[i] == solution[j]:
                    return False

        return True


class ColorMapProblemTest(TestCase):

    def test(self):
        space = Domain[ColorMapProblem]()

        @replay_function
        def ______():
            solution, _ = space.get_sample()

            for i, row in enumerate(solution.map):
                for j, item in enumerate(row):
                    assert item == solution.map[j][i]

            @replay_function
            def ______():
                is_good = solution.validate_solution()


#################################################################
#                                                               #
#                N Queens Test                                  #
#                                                               #
#################################################################

@FunctionalConstraint
def FreePositions(n, queens):
    table = [(i, j) for i in range(n) for j in range(n)]

    def free_place(place, queen): return (
        place[0] - queen[0] == place[1] - queen[1]
        or place[0] == queen[0]
        or queen[1] == place[1]
    )
    result = [pos for pos in table
              for queen in queens
              if free_place(pos, queen)]
    return result if len(result) > 0 else table


class NQueenProblem:
    NDomain = Domain[int](max=20)

    def __init__(self, n: int = NDomain) -> None:
        self.n = n

    SolutionDomain = Domain[int][NDomain][2] | (
        lambda x, i, n=NDomain: (
            x[i][0] < n,
            x[i][1] < n,
            x[i] == FreePositions(n, x[:i-1])
        )
    )

    def validate_solution(self, solution: List[List[int]] = SolutionDomain):
        assert len(solution) == len(self.n)

        for pos in solution:
            assert pos[0] < self.n
            assert pos[1] < self.n

        def free_place(place, queen): return (
            place[0] - queen[0] == place[1] - queen[1]
            or place[0] == queen[0]
            or queen[1] == place[1]
        )

        for i, q1 in enumerate(solution):
            for j, q2 in enumerate(solution):
                if i != j and not free_place(q1, q2):
                    return False
        return True


class NQueenProblemTest(TestCase):

    def test(self):
        space = Domain[NQueenProblem]()

        @replay_function
        def ______():
            solution, _ = space.get_sample()

            @replay_function
            def ______():
                is_good = solution.validate_solution()
