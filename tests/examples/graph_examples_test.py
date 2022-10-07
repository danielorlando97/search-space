from typing import List, Optional
from typing_extensions import Self
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function


class GraphByAdjMatrix:
    NDomain = Domain[int]()
    AdjMatrixDomain = Domain[bool][NDomain][NDomain] | (
        lambda x, i, j: x[i][j] == x[j][i]
    )

    def __init__(
        self,
        n: int = NDomain,
        adj_matrix: List[int] = AdjMatrixDomain
    ) -> None:
        self.n, self.matrix = n, adj_matrix


class GraphByAdjMatrixTest(TestCase):

    def test(self):
        space = Domain[GraphByAdjMatrix]() | (
            lambda x: x.NDomain < 20
        )

        @replay_function
        def ______():
            graph, _ = space.get_sample()

            assert len(graph.matrix) == graph.n


class Node:
    RightDomain = Domain[Optional[Self]]()
    LeftDomain = Domain[Optional[Self]]()

    def __init__(
        self,
        right: Self = RightDomain,
        left: Self = LeftDomain
    ) -> None:
        self.right, self.left = right, left


class GraphByNodeTest(TestCase):

    def test(self):
        space = Domain[Node]() | (
            lambda x: (
                x.RightDomain == None,
                x.LeftDomain != None
            )
        )

        @replay_function
        def ______():
            graph, _ = space.get_sample()

            assert isinstance(graph, Node)
            assert isinstance(graph.left, Node)
            assert graph.right is None
