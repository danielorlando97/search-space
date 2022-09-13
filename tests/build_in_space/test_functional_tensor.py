from search_space.sampler.distribution_names import UNIFORM
from search_space.sampler.factory import SamplerFactory
from search_space.spaces.build_in_spaces import TensorSearchSpace as Tensor
from search_space.spaces.build_in_spaces import NaturalSearchSpace as N
from search_space.spaces.build_in_spaces import CategoricalSearchSpace as Categorical
from tests.config import validate_replay_count
import pytest


@pytest.mark.slow
def test_random_values():
    a, b = 1, 1000
    space_type = N(a, b)
    space_type.set_sampler(SamplerFactory().create_sampler(
        UNIFORM, search_space=space_type))

    shape_space = N(a, b)
    shape_space.set_sampler(
        SamplerFactory().create_sampler(UNIFORM, search_space=shape_space))

    n = Tensor(space_type=space_type, shape_space=(shape_space))

    for _ in range(validate_replay_count):
        v1, _ = n.get_sample()
        v2, _ = n.get_sample()

        assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"


@pytest.mark.slow
def test_context_consistence():
    a, b = 1, 1000
    space_type = N(a, b)
    space_type.set_sampler(SamplerFactory().create_sampler(
        UNIFORM, search_space=space_type))

    shape_space = N(a, b)
    shape_space.set_sampler(
        SamplerFactory().create_sampler(UNIFORM, search_space=shape_space))

    n = Tensor(space_type=space_type, shape_space=(shape_space))

    v1, context = n.get_sample()
    values_list = [n.get_sample(context=context) for _ in range(20)]
    values_list = [v for v, _ in values_list if v != v1]

    assert not any(values_list), """
        The same sampler generates the same value for the same context"""


@pytest.mark.slow
def test_natural_minimal_number_space():
    a, b = 10, 1000
    space_type = N(a, b)
    space_type.set_sampler(SamplerFactory().create_sampler(
        UNIFORM, search_space=space_type))

    shape_space = N(a, b)
    shape_space.set_sampler(
        SamplerFactory().create_sampler(UNIFORM, search_space=shape_space))

    n = Tensor(space_type=space_type, shape_space=(shape_space))

    for _ in range(validate_replay_count):
        value, context = n.get_sample()
        l, _ = shape_space.get_sample(context=context)
        assert len(value) == l
        assert value == [v for v in value if v % 1 == 0]
        assert value != [v for v in value if v == value[0]]


@pytest.mark.slow
def test_natural_minimal_categorical_space():
    categories = [i for i in range(1000)]
    a, b = 10, 1000

    space_type = Categorical(*categories)
    space_type.set_sampler(SamplerFactory().create_sampler(
        UNIFORM, search_space=space_type))

    shape_space = N(a, b)
    shape_space.set_sampler(
        SamplerFactory().create_sampler(UNIFORM, search_space=shape_space))

    n = Tensor(space_type=space_type, shape_space=(shape_space))

    for _ in range(validate_replay_count):
        value, context = n.get_sample()
        l, _ = shape_space.get_sample(context=context)
        assert len(value) == l
        assert value == [v for v in value if v in categories]
        assert value != [v for v in value if v == value[0]]


# def test_tensor_dynamical_lens():
#     l1 = N(1, 10)
#     l2 = N(1, 10)
#     l3 = N(1, 10)
#     n = Tensor(space_type=N(0, 10), shape_space=(l1, l2, l3))

#     v1, _ = n.get_sample()
#     v2, _ = n.get_sample()

#     assert v1 != v2, "a random variable, if the space is sufficiently large then all sequential samples must be different"

#     v1, context = n.get_sample()
#     values_list = [n.get_sample(context=context) for _ in range(20)]
#     values_list = [v for v, _ in values_list if v != v1]

#     assert not any(values_list), """
#     The same sampler generates the same value for the same context"""

#     for _ in range(validate_replay_count):
#         vl1, context = l1.get_sample()
#         vl2, _ = l2.get_sample(context=context)
#         vl3, _ = l3.get_sample(context=context)
#         value, _ = n.get_sample(context=context)
#         assert len(value) == vl1
#         assert len(value[0]) == vl2
#         assert len(value[0][0]) == vl3
#         for matrix in value:
#             for row in matrix:
#                 for v in row:
#                     assert v % 1 == 0, 'values should be integers'
#                     assert v <= 10


# def test_tensor_dsl_minimal():
#     n = Tensor(space_type=N(0, 10), shape_space=(10))
#     n |= (lambda i, x: x[i % 3 == 0] < 3)

#     for _ in range(validate_replay_count):
#         value, _ = n.get_sample()
#         for i, v in enumerate(value):
#             assert i % 3 != 0 or v < 3
