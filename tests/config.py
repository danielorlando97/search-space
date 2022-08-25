import os

validate_replay_count = os.getenv('validate_replay_count', '')
if any(validate_replay_count):
    validate_replay_count = int(validate_replay_count)
else:
    validate_replay_count = 100
