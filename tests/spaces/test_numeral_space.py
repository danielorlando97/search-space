from search_space import distribution_names as df
from search_space import NaturalSearchSpace as N
from search_space import ContinueSearchSpace as R
from search_space import UniversalVariable as x
from tests.config import validate_replay_count


def test_natural_space():
    n = N(0, 10000000, distribute_like=df.UNIFORM)

    v1, _ = n.get_sampler()
    v2, _ = n.get_sampler()

    assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"

    v1, context = n.get_sampler()
    values_list = [n.get_sampler(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(
        values_list), "The same sampler generates the same value for the same context"

    n = N(10, 20)

    assert validate_replay_count > 30, "30 is the minimal number to validate a random process"

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value % 1 == 0, 'values should be integers'
        assert 10 <= value and value <= 20


def test_real_space():
    n = R(0, 10000000, distribute_like=df.UNIFORM)

    v1, _ = n.get_sampler()
    v2, _ = n.get_sampler()

    assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"

    v1, context = n.get_sampler()
    values_list = [n.get_sampler(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(
        values_list), "The same sampler generates the same value for the same context"

    ten_values = [n.get_sampler() for _ in range(10)]
    ten_values = [v for v, _ in ten_values if v % 1 != 0]

    assert any(ten_values), "Any value has be a float value"

    n = R(10, 20)

    assert validate_replay_count > 30, "30 is the minimal number to validate a random process"

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert 10 <= value and value <= 20


def test_lt_constraint_dsl():
    """Real Space Test"""
    n = R() | (x < 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value < 5

    """Natural Space Test"""
    n = N() | (x < 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value < 5

    """Context Sensitive Test"""
    n = N() | (1 < x, x < 10)
    m = R() | (x < n)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        assert nv < 10
        assert mv < nv


def test_le_constraint_dsl():
    """Real Space Test"""
    n = R() | (x <= 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value <= 5

    """Natural Space Test"""
    n = N() | (x <= 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value <= 5

    """Context Sensitive Test"""
    n = N() | (1 <= x, x <= 10)
    m = R() | (x <= n)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        assert nv <= 10
        assert mv <= nv


def test_gt_constraint_dsl():
    """Real Space Test"""
    n = R(0, 10) | (x > 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value > 5

    """Natural Space Test"""
    n = N(0, 10) | (x > 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value > 5

    """Context Sensitive Test"""
    n = N(0, 10) | (9 > x, x > 5)
    m = R() | (x > n)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        assert nv > 5
        assert mv > nv


def test_ge_constraint_dsl():
    """Real Space Test"""
    n = R(0, 10) | (x >= 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value >= 5

    """Natural Space Test"""
    n = N(0, 10) | (x >= 5)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value >= 5

    """Context Sensitive Test"""
    n = N(0, 10) | (9 >= x, x >= 5)
    m = R() | (x >= n)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        assert nv >= 5
        assert mv >= nv
