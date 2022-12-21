test-fast:
	export validate_replay_count=100 && python -m pytest search_space tests -v --tb=short -m "not time" --slow-last

test: 
	export validate_replay_count=${replay_num} && python -m pytest search_space tests -v --tb=short --slow-last

test-full:
	export validate_replay_count=100000 && python -m pytest search_space tests -v --tb=short --slow-last

test-syntax:
	export validate_replay_count=100 && python -m pytest search_space tests -v --tb=short --slow-last --ignore=tests/examples --ignore=tests/dsl_e2e

base-test:
	export validate_replay_count=${replay_num} && python -m pytest search_space tests -v --tb=short --slow-last --ignore=tests/examples --ignore=tests/dsl_e2e

dsl-test:
	export validate_replay_count=${replay_num} && python -m pytest search_space tests -v --tb=short --slow-last --ignore=tests/examples --ignore=tests/basic_domains --ignore=tests/constraint

example-test:
	export validate_replay_count=${replay_num} && python -m pytest search_space tests -v --tb=short --slow-last --ignore=tests/dsl_e2e --ignore=tests/basic_domains --ignore=tests/constraint

exp_set:
	./run_exp.sh -n 100 -e set -i 1000 

exp_set_2:
	./run_exp.sh -n 100 -e set2 -i 1000 

exp_matrix:
	./run_exp.sh -n 100 -e matrix -i 100 

exp_even:
	./run_exp.sh -n 100 -e even -i 500000 

exp_even_fixed:
	./run_exp.sh -n 1 -e even_fixed -i 500000

center:
	./run_exp.sh -n 1 -e center -i 100