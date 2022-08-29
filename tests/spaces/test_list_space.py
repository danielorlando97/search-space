from search_space import ListSearchSpace as Array
from search_space import NaturalSearchSpace as N
from search_space import ContinueSearchSpace as R
from search_space import UniversalVariable as x
from search_space import UniversalIndex as i
from tests.config import validate_replay_count
from search_space.spaces.build_in_spaces.object_search_space import MetaClassFabricSearchSpace


natural_array_space = Array(
    type_space=N() | (x < 1000000), len_space=N(10, 20))
# natural_array_space |= (x[1] < 3, x[i != 1] < 2, x[i] <= x[i + 1])
natural_array_space |= (x[i] <= x[i + 1])


def test_list_space():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))

    real_array_space = Array(
        type_space=R(), len_space=N(2, 10))

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert natural_list == [v for v in natural_list if v % 1 == 0]
        assert any([v for v in natural_list if v != natural_list[0]])

        real_list, _ = real_array_space.get_sampler()

        assert len(real_list) <= 10
        assert any([v for v in real_list if v != real_list[0]])

# TODO: (x < 10) raise error


def test_lt_constraint_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[i] < 10)

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert natural_list == [v for v in natural_list if v < 10]


def test_le_constraint_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[i] <= 10)

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert natural_list == [v for v in natural_list if v <= 10]


def test_gt_constraint_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[i] > 10)

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert natural_list == [v for v in natural_list if v > 10]


def test_ge_constraint_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[i] >= 10)

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert natural_list == [v for v in natural_list if v >= 10]


def test_predication_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[i % 2 == 0] < 1)

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert 0 == sum([
            v for i, v in enumerate(natural_list) if i % 2 == 0])
        assert sum(natural_list) > 0


def test_specific_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[0] < 1)

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert 0 == natural_list[0]
        assert sum(natural_list) > 0

# TODO


def test_sequence_dsl():
    natural_array_space = Array(
        type_space=N(), len_space=N(2, 10))
    natural_array_space |= (x[i] <= x[i + 1])

    for _ in range(validate_replay_count):
        natural_list, _ = natural_array_space.get_sampler()

        assert len(natural_list) <= 10
        assert natural_list == [natural_list[i] for i in range(
            len(natural_list) - 1) if natural_list[i] <= natural_list[i + 1]] + [natural_list[-1]]

    # natural_array_space = Array(
    #     type_space=N(), len_space=N(2, 10))
    # natural_array_space |= (x[i] <= x[i - 1])

    # for _ in range(validate_replay_count):
    #     natural_list, _ = natural_array_space.get_sampler()

    #     assert len(natural_list) <= 10
    #     assert natural_list == [natural_list[0]] + [natural_list[i] for i in range(
    #         1, len(natural_list)) if natural_list[i] <= natural_list[i - 1]]


def test_matrix_space():

    natural_matrix_space = Array(
        type_space=Array(type_space=N(), len_space=N(10, 10)), len_space=N(2, 10))

    for _ in range(validate_replay_count):
        natural_matrix, _ = natural_matrix_space.get_sampler()

        assert len(natural_matrix) <= 10
        assert natural_matrix == [
            row for row in natural_matrix if len(row) == 10]

        assert len(natural_matrix) * \
            10 == len([item for row in natural_matrix for item in row])


class Line(metaclass=MetaClassFabricSearchSpace):
    """Domain Description"""
    m_domain = R()
    n_domain = R()
    x_domain = R()

    """Class Description"""

    def __init__(self, m: float = m_domain, n: float = n_domain) -> None:
        self.m, self.n = m, n

    def get_point(self, x: float = x_domain):
        return (x, self.m * x + self.n)


def test_list_object():
    line_list_space = Array(
        type_space=Line(), len_space=N(2, 10))

    for _ in range(validate_replay_count):
        line_list, _ = line_list_space.get_sampler()

        assert len(line_list) <= 10
        assert len(line_list) == len([
            item for item in line_list if type(item) == Line])
        assert 0 != len(
            [item for item in line_list if item.m != line_list[0].m])
        assert 0 != len(
            [item for item in line_list if item.n != line_list[0].n])
