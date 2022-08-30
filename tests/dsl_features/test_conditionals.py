from search_space import ListSearchSpace as Array
from search_space import NaturalSearchSpace as N
from search_space import ContinueSearchSpace as R
from search_space import CategoricalSearchSpace as Choice
from search_space import UniversalVariable as x
from search_space import UniversalIndex as i
from tests.config import validate_replay_count


def test_numeral_conditional():
    n = N() | ((False) >> (x < 1))
    r = R() | ((True) >> (x < 1))

    for _ in range(validate_replay_count):
        nv, _ = n.get_sampler()
        rv, _ = r.get_sampler()
        assert nv > 0
        assert rv < 1

    n = N() | (x < 10)
    r = R() | ((5 > n) >> (x < 1))

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        rv, _ = r.get_sampler(context)
        assert nv < 10
        assert nv <= 5 or r < 1


def test_categorical_conditional():
    n = Choice(1, 2, 3, 4) | ((False) >> (x < 1))
    r = Choice(1, 2, 3, 4) | ((True) >> (x < 2))

    for _ in range(validate_replay_count):
        nv, _ = n.get_sampler()
        rv, _ = r.get_sampler()
        assert nv in [1, 2, 3, 4]
        assert rv < 2

    n = Choice(1, 2, 3, 4) | ((False) >> (x < 1))
    r = Choice(1, 2, 3, 4) | ((n > 2) >> (x < 2))

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        rv, _ = r.get_sampler(context)
        assert nv <= 2 or r < 2


def test_list_conditional():

    n = Array(type_space=Choice(1, 2, 3, 4), len_space=N(
        2, 10)) | ((x[i+1] > 2) >> (x[i] < 3))

    for _ in range(validate_replay_count):
        nv, _ = n.get_sampler()

        for j in range(len(nv)):
            if j + 1 < len(nv) and nv[j + 1] > 2:
                assert nv[j] < 3


# TODO: test object
