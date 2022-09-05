from search_space import dsl as ss
from tests.config import validate_replay_count


def test_tensor_natural_minimal():
    n = ss.Tensor(space_type=ss.N(0, 10), shape_space=(10))

    v1, _ = n.get_sample()
    v2, _ = n.get_sample()

    assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"

    v1, context = n.get_sample()
    values_list = [n.get_sample(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(values_list), """
    The same sampler generates the same value for the same context"""

    for _ in range(validate_replay_count):
        value, _ = n.get_sample()
        assert len(value) == 10
        for v in value:
            assert v % 1 == 0, 'values should be integers'
            assert v <= 10


def test_tensor_dynamical_lens():
    l1 = ss.N(1, 10)
    l2 = ss.N(1, 10)
    l3 = ss.N(1, 10)
    n = ss.Tensor(space_type=ss.N(0, 10), shape_space=(l1, l2, l3))

    v1, _ = n.get_sample()
    v2, _ = n.get_sample()

    assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"

    v1, context = n.get_sample()
    values_list = [n.get_sample(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(values_list), """
    The same sampler generates the same value for the same context"""

    for _ in range(validate_replay_count):
        vl1, context = l1.get_sample()
        vl2, _ = l2.get_sample(context=context)
        vl3, _ = l3.get_sample(context=context)
        value, _ = n.get_sample(context=context)
        assert len(value) == vl1
        assert len(value[0]) == vl2
        assert len(value[0][0]) == vl3
        for matrix in value:
            for row in matrix:
                for v in row:
                    assert v % 1 == 0, 'values should be integers'
                    assert v <= 10


# def test_natural_dsl_constraint():
#     n = N() | (lambda x: (x < 10))

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sample()
#         assert value % 1 == 0, 'values should be integers'
#         assert value < 10
