from search_space import dsl as ss
from tests.config import validate_replay_count, margin_time
from time import time
from random import choice, randint
import pytest


def random_list(_len, func):
    result = []
    for _ in range(_len):
        result.append(func())

    return result

@pytest.mark.slow
@pytest.mark.time
def test_time_comp_number_space():
    a, b = 1, 1000000000

    start = time()
    for i in range(validate_replay_count):
        _ = random_list(i, lambda: randint(a, b))

    random_time = start - time()

    n = ss.Tensor(space_type=ss.N(a, b), shape_space=(0))
    start = time()
    for i in range(validate_replay_count):
        n.len_spaces = [i]
        _ = n.get_sample()

    space_time = start - time()

    assert random_time * margin_time > space_time

@pytest.mark.slow
@pytest.mark.time
def test_time_comp_categorical_space():
    categories = [i for i in range(1000)]

    start = time()
    for i in range(validate_replay_count):
        _ = random_list(i, lambda: choice(categories))

    random_time = start - time()

    n = ss.Tensor(space_type=ss.Categorical(*categories), shape_space=(0))
    start = time()
    for i in range(validate_replay_count):
        n.len_spaces = [i]
        _ = n.get_sample()

    space_time = start - time()

    assert random_time * margin_time > space_time


@pytest.mark.slow
@pytest.mark.time
def test_time_comp_matrix_space():
    a, b = 1, 1000000000

    start = time()
    for i in range(validate_replay_count):
        _ = random_list(i, lambda: random_list(i, lambda: randint(a, b)))

    random_time = start - time()

    n = ss.Tensor(space_type=ss.N(a, b), shape_space=(0, 0))
    start = time()
    for _ in range(validate_replay_count):
        n.len_spaces = [i, i]
        _ = n.get_sample()

    space_time = start - time()

    assert random_time * margin_time > space_time
