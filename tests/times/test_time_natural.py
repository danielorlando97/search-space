from search_space import dsl as ss
from tests.config import validate_replay_count, margin_time
from time import time
from random import randint
import pytest


@pytest.mark.time
def test_time_comp():
    a, b = 0, 100000000000

    start = time()
    for _ in range(validate_replay_count):
        _ = randint(a, b)

    random_time = start - time()

    n = ss.N(a, b)
    start = time()
    for _ in range(validate_replay_count):
        _ = n.get_sample()

    space_time = start - time()

    assert random_time * margin_time > space_time