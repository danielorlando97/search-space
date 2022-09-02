from search_space import NaturalSearchSpace as N
from search_space import ContinueSearchSpace as R
from tests.config import validate_replay_count


def test_natural_minimal():
    n = N(0, 100000000000)

    v1, _ = n.get_sample()
    v2, _ = n.get_sample()

    assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"

    v1, context = n.get_sample()
    values_list = [n.get_sample(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(values_list), """
    The same sampler generates the same value for the same context"""

    n = N(10, 100)

    for _ in range(validate_replay_count):
        value, _ = n.get_sample()
        assert value % 1 == 0, 'values should be integers'
        assert 10 <= value and value <= 100


def test_natural_dsl_constraint():
    n = N() | (lambda x: (x < 10))

    for _ in range(validate_replay_count):
        value, _ = n.get_sample()
        assert value % 1 == 0, 'values should be integers'
        assert value < 10
