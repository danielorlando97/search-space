import os

from search_space.context_manager.runtime_manager import SearchSpaceConfig

SearchSpaceConfig(
    verbose=False,
    replay_nums=100,
    minimal_numeral_limit=-10000,
    maximal_numeral_limit=1000
)

validate_replay_count = os.getenv('validate_replay_count', '')
if any(validate_replay_count):
    validate_replay_count = int(validate_replay_count)
else:
    validate_replay_count = 100


margin_time = os.getenv('margin_time', '')
if any(margin_time):
    margin_time = int(margin_time)
else:
    margin_time = 1.5


def replay_function(func):
    for _ in range(validate_replay_count):
        func()
