from search_space import ListSearchSpace as Array
from search_space import NaturalSearchSpace as N
from search_space import ContinueSearchSpace as R
from search_space import UniversalVariable as x
from search_space import UniversalIndex as i
from tests.config import validate_replay_count


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
        assert len(natural_matrix) == [
            row for row in natural_matrix if len(row) == 10]

        assert len(natural_matrix) * \
            10 == len([item for row in natural_matrix for item in row])
