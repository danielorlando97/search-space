import os

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
