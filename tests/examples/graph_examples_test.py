from typing import List, Optional
from typing_extensions import Self
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function, validate_replay_count


class GraphByAdjMatrix:
    NDomain = Domain[int](min=0, max=1000)
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
            for i, row in enumerate(graph.matrix):
                assert len(row) == graph.n
                for j, item in enumerate(row):
                    assert item == graph.matrix[j][i]


class Node:
    RightDomain = Domain[Optional[Self]]()
    LeftDomain = Domain[Optional[Self]]() | (
        lambda x: x.LeftDomain == None
    )

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
            )
        )

        def dfs(node):
            assert isinstance(node, Node)
            assert node.right is None
            if node.left != None:
                dfs(node.left)

        count = 0

        @replay_function
        def ______():
            nonlocal count

            try:
                graph, _ = space.get_sample()
                dfs(graph)
            except RecursionError:
                count += 1

        assert count <= validate_replay_count / \
            2, (count,  validate_replay_count)
