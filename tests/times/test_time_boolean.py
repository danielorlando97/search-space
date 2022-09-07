from search_space import dsl as ss
from tests.config import validate_replay_count, margin_time
from time import time
from random import random
import pytest


@pytest.mark.time
def test_time_comp():
    start = time()
    for _ in range(validate_replay_count):
        _ = True if random() > 0.5 else False

    random_time = start - time()

    n = ss.Bool()
    start = time()
    for _ in range(validate_replay_count):
        _ = n.get_sample()

    space_time = start - time()

    assert random_time * margin_time > space_time
