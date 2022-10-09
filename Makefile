test-fast:
	export validate_replay_count=100 && python -m pytest search_space tests -v --tb=short -m "not time" --slow-last

test: 
	export validate_replay_count=${replay_num} && python -m pytest search_space tests -v --tb=short --slow-last

test-full:
	export validate_replay_count=100000 && python -m pytest search_space tests -v --tb=short --slow-last

test-syntax:
	export validate_replay_count=100 && python -m pytest search_space tests -v --tb=short --slow-last --ignore=tests/examples --ignore=tests/dsl_e2e