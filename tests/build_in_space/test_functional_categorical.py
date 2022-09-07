from search_space import dsl as ss
from tests.config import validate_replay_count


def test_random_values():
    categories = [i for i in range(1000)]
    n = ss.Categorical(*categories)

    for _ in range(validate_replay_count):
        v1, _ = n.get_sample()
        v2, _ = n.get_sample()

        assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"


def test_context_consistence():
    categories = [i for i in range(1000)]
    n = ss.Categorical(*categories)

    v1, context = n.get_sample()
    values_list = [n.get_sample(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(values_list), """
        The same sampler generates the same value for the same context"""


def test_natural_minimal():
    values = ['white', 'black', 'red']
    n = ss.Categorical(*values)

    for _ in range(validate_replay_count):
        value, _ = n.get_sample()
        assert value in values


# def test_dsl_constraint():
#     func = [
#         ("Less", lambda x: x < 50),
#         ("LessEq", lambda x: x <= 50),
#         ("Great", lambda x: x > 50),
#         ("GreatEq", lambda x: x >= 50)
#     ]

#     for op, f in func:
#         n = ss.N(0, 100) | f
#         for _ in range(validate_replay_count):
#             value, _ = n.get_sample()
#             assert f(value), f'Error with operator {op}'


# def test_dsl_context_sensitive():
#     m = ss.N(40, 60)

#     func = [
#         ("Less", lambda x: x < m, lambda x, y: x < y),
#         ("LessEq", lambda x: x <= m, lambda x, y: x <= y),
#         ("Great", lambda x: x > m, lambda x, y: x > y),
#         ("GreatEq", lambda x: x >= m, lambda x, y: x >= y)
#     ]

#     for op, f, test in func:
#         n = ss.N(0, 100) | f
#         for _ in range(validate_replay_count):
#             value, context = n.get_sample()
#             m_value, _ = m.get_sample(context=context)
#             assert test(
#                 value, m_value), f'Error with operator {op} => ({value}, {m_value})'
