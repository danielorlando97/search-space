from search_space import dsl as ss
from tests.config import validate_replay_count, margin_time
from time import time
from random import choice
import pytest


@pytest.mark.time
def test_time_comp():
    categories = [i for i in range(1000)]
    start = time()
    for _ in range(validate_replay_count):
        _ = choice(categories)

    random_time = start - time()

    n = ss.Categorical(*categories)
    start = time()
    for _ in range(validate_replay_count):
        _ = n.get_sample()

    space_time = start - time()

    assert random_time * margin_time > space_time
