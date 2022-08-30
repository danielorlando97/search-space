from search_space import CategoricalSearchSpace as Choice
from search_space import BooleanSearchSpace as Boolean
from search_space import UniversalVariable as x
from tests.config import validate_replay_count


def test_categorical_space():
    color = Choice("white", 'black', "red")
    number = Choice(1, 10, 100)

    v1, context = color.get_sampler()
    values_list = [color.get_sampler(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(
        values_list), "The same sampler generates the same value for the same context"

    for _ in range(validate_replay_count):
        value, _ = color.get_sampler()
        value1, _ = number.get_sampler()
        assert value in ["white", 'black', "red"]
        assert value1 in [1, 10, 100]


def test_boolean_space():
    bool_ = Boolean()

    v1, context = bool_.get_sampler()
    values_list = [bool_.get_sampler(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(
        values_list), "The same sampler generates the same value for the same context"

    for _ in range(validate_replay_count):
        value, _ = bool_.get_sampler()
        assert value in [True, False]


def test_lt_constraint_dsl():
    """Real Space Test"""
    n = Choice(1, 10, 100) | (x < 20)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value < 20

    """Real Space Test"""
    n = Choice("a", "b", "c", "d") | (x < "c")

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value in ["a", "b"]

    """Context Sensitive Test"""
    n = Choice("a", "b", "c", "d") | ("a" < x, x < "d")
    m = Choice("a", "b", "c", "d") | (x < n)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        assert nv in ["b", "c"]
        assert mv in ['b', 'a']


def test_gt_constraint_dsl():
    """Real Space Test"""
    n = Choice(1, 10, 100) | (x > 20)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value > 20

    """Real Space Test"""
    n = Choice("a", "b", "c", "d") | (x > "c")

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value in ["d"]

    """Context Sensitive Test"""
    n = Choice("a", "b", "c", "d") | ("a" < x, x < "d")
    m = Choice("a", "b", "c", "d") | (x > n)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        assert nv in ["b", "c"]
        assert mv in ['b', "c", "d"]


def test_eq_ne_dsl():
    """Real Space Test"""
    n = Choice(1, 10, 100) | (x != 10)

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value in [1, 100]

    """Real Space Test"""
    n = Choice("a", "b", "c", "d") | (x == "c")

    for _ in range(validate_replay_count):
        value, _ = n.get_sampler()
        assert value == 'c'

    """Context Sensitive Test"""
    n = Choice("a", "b", "c", "d") | ("a" < x, x < "d")
    m = Choice("a", "b", "c", "d") | (x != n)
    k = Choice("a", "b", "c", "d") | (x == m)

    for _ in range(validate_replay_count):
        nv, context = n.get_sampler()
        mv, _ = m.get_sampler(context)
        kv, _ = k.get_sampler(context)
        assert nv in ["b", "c"]
        assert mv != nv
        assert kv == mv

# def test_le_constraint_dsl():
#     """Real Space Test"""
#     n = R() | (x <= 5)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sampler()
#         assert value <= 5

#     """Natural Space Test"""
#     n = N() | (x <= 5)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sampler()
#         assert value <= 5

#     """Context Sensitive Test"""
#     n = N() | (1 <= x, x <= 10)
#     m = R() | (x <= n)

#     for _ in range(validate_replay_count):
#         nv, context = n.get_sampler()
#         mv, _ = m.get_sampler(context)
#         assert nv <= 10
#         assert mv <= nv


# def test_gt_constraint_dsl():
#     """Real Space Test"""
#     n = R(0, 10) | (x > 5)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sampler()
#         assert value > 5

#     """Natural Space Test"""
#     n = N(0, 10) | (x > 5)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sampler()
#         assert value > 5

#     """Context Sensitive Test"""
#     n = N(0, 10) | (9 > x, x > 5)
#     m = R() | (x > n)

#     for _ in range(validate_replay_count):
#         nv, context = n.get_sampler()
#         mv, _ = m.get_sampler(context)
#         assert nv > 5
#         assert mv > nv


# def test_ge_constraint_dsl():
#     """Real Space Test"""
#     n = R(0, 10) | (x >= 5)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sampler()
#         assert value >= 5

#     """Natural Space Test"""
#     n = N(0, 10) | (x >= 5)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sampler()
#         assert value >= 5

#     """Context Sensitive Test"""
#     n = N(0, 10) | (9 >= x, x >= 5)
#     m = R() | (x >= n)

#     for _ in range(validate_replay_count):
#         nv, context = n.get_sampler()
#         mv, _ = m.get_sampler(context)
#         assert nv >= 5
#         assert mv >= nv
