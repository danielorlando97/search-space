from typing import Optional, Union
from typing import List, Optional, Union
from typing_extensions import Self
from unittest import TestCase
from search_space.dsl import Domain, RandomValue
from search_space.spaces import FunctionalConstraint
from tests.config import replay_function, validate_replay_count


class Set:
    NDomain = Domain[int](min=0, max=1000)

    def __init__(
        self,
        # The DSL defines a syntax similar to that of
        # statically typed languages for defining tensor types.
        # But in this case the dimension does not necessarily
        # have to be a fixed value.
        values: List[int] = Domain[int][NDomain] | (

            # Comparison operators also support lists as second operators.
            # And as long as the constraint does not make comparisons of type
            # x == x the system can find the topological order of the described sequence.
            lambda x, i: x[i] != x[:i]
        )
    ) -> None:
        self.values = values


class GraphByAdjMatrix:
    NDomain = Domain[int](min=0, max=1000)

    def __init__(
        self, n: int = NDomain,
        adj_matrix: List[int] = Domain[bool][NDomain][NDomain] | (
            # The DSL design pattern in principle does not allow circular dependencies,
            # except for circular constraints internal to a structure (class or tensor).
            # In these cases, since the native comparators are symmetric,
            # the system simply ignores one of the edges.
            lambda x, i, j: x[i][j] == x[j][i]
        )
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


# There are many constraints that cannot be expressed
# as a combination of the operations defined by the DSL grammar.
# Therefore, a mechanism for expressing imperative constraints is needed.

@FunctionalConstraint
def if_is_int_then_is_even(x):
    if type(x) != int:
        return True

    for i in range(2, x//2 + 1):
        if x % i == 0:
            return False
    return True


class Sum:
    def __init__(
        self,
        a: Union[Self, int] = Domain[Union[Self, int]] | (
            # Imperative restrictions on which parameters they depend
            # will be considered as black box functions or
            # natural values that can be aggregated
            # to the dynamic domain inheritance process.
            lambda x: if_is_int_then_is_even(x)
        ),

        # The DSL implements an integration with the typing library
        # to describe recursive spaces, multi-type spaces and optional spaces.
        b: Union[Self, int] = Domain[Union[Self, int]] | (
            lambda x: if_is_int_then_is_even(x)
        )
    ) -> None:
        self.a, self.b = a, b


optional_summation_space = Domain[Optional[Sum]]()


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
