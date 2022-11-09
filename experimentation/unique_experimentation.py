# %%
import csv
from time import time
import matplotlib.pyplot as plt
from search_space.dsl import Domain
from search_space.spaces import FunctionalConstraint
from search_space.context_manager import SearchSpaceConfig
from search_space.utils.infinity import oo
from . import tools
from search_space.sampler.default_implementations import UniformSampler
from search_space.spaces.domains import NaturalDomain

config = SearchSpaceConfig()
config.replay_nums = oo

#################################################################
#                                                               #
#                  Set Randint                                  #
#                                                               #
#################################################################


def set_randint(_iter=9500, n=''):
    a, b = 0, _iter + 1
    header = ['iter_num', 'time', 'attempts']

    def experiment(i):
        result = []
        attempts = 0
        start = time()
        for _ in range(i):
            value = tools.randint(a, b)
            while value in result:
                attempts += 1
                value = tools.randint(a, b)
                # if attempts > _iter:
                #     break
            result.append(value)
        return [i, time() - start, attempts]

    data = tools.run_test(experiment, _iter, f"Set Randint Experimentation{n}")
    tools.save_csv(header, data, f'set_randint_data')


#################################################################
#                                                               #
#                  Set DSL                                      #
#                                                               #
#################################################################
def dsl_set(_iter=9500, n=''):
    a, b = 0, _iter + 1
    header = ['iter_num', 'time', 'attempts']
    data = []

    def experiment(size):
        d = Domain[int][size](min=a, max=b) | (lambda x, i: x[i] != x[0: i])
        config.attempts = []
        start = time()
        _ = d. get_sample()
        return [size, time() - start, len(config.attempts)]

    data = tools.run_test(experiment, _iter, f"Set DSL Experimentation{n}")
    tools.save_csv(header, data, f'set_dsl_data')


#################################################################
#                                                               #
#                  Set 2 Randint                                #
#                                                               #
#################################################################
def set_2_randint(_iter=9500, n=''):
    a, b = 0, _iter + 1
    header = ['iter_num', 'time', 'attempts']

    def experiment(i):
        result = []
        attempts = 0
        start = time()
        for _ in range(i):
            value = tools.randint(a, i + 2)
            while value in result:
                attempts += 1
                value = tools.randint(a, i + 2)
                # if attempts > _iter:
                #     break
            result.append(value)
        return [i, time() - start, attempts]

    data = tools.run_test(experiment, _iter, f"Set Randint Experimentation{n}")
    tools.save_csv(header, data, f'set_2_randint_data')


#################################################################
#                                                               #
#                  Set 2 DSL                                    #
#                                                               #
#################################################################
def dsl_2_set(_iter=9500, n=''):
    a, b = 0, _iter + 1
    header = ['iter_num', 'time', 'attempts']
    data = []

    def experiment(size):
        d = Domain[int][size](
            min=a, max=size + 2) | (lambda x, i: x[i] != x[0: i])
        config.attempts = []
        start = time()
        _ = d. get_sample()
        return [size, time() - start, len(config.attempts)]

    data = tools.run_test(experiment, _iter, f"Set DSL Experimentation{n}")
    tools.save_csv(header, data, f'set_2_dsl_data')


#################################################################
#                                                               #
#                  Matrix Randint                               #
#                                                               #
#################################################################
def matrix_randint(_iter=9500, n=''):
    a, b = 0, 100000
    header = ['iter_num', 'time', 'attempts']

    def experiment(size):
        result = [[0] * (size + 1) for _ in range(size + 1)]
        attempts = 0
        start = time()
        for i in range(size + 1):
            for j in range(i, size + 1):
                value = tools.randint(a, b)
                result[i][j] = value
                result[j][i] = value

        return [i, time() - start, attempts]

    data = tools.run_test(
        experiment, _iter, f"Matrix Randint Experimentation{n}")
    tools.save_csv(header, data, f'matrix_randint_data')


#################################################################
#                                                               #
#                  Matrix DSL                                   #
#                                                               #
#################################################################
def dsl_matrix(_iter=9500, n=''):
    a, b = 0, 100000
    header = ['iter_num', 'time', 'attempts']
    data = []

    def experiment(size):
        d = Domain[int][size+1][size + 1](min=a, max=b) | (
            lambda x, i, j: x[i][j] == x[j][i]
        )

        config.attempts = []
        start = time()
        _ = d. get_sample()
        return [size, time() - start, len(config.attempts)]

    data = tools.run_test(experiment, _iter, f"Matrix DSL Experimentation{n}")
    tools.save_csv(header, data, f'matrix_dsl_data')


#################################################################
#                                                               #
#                  Even Find Randint                            #
#                                                               #
#################################################################


def is_even(x: int):
    for i in range(2, x//2 + 1):
        if x % i == 0:
            return False
    return True


def even_find_randint(_iter=10000):

    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']

    def experiment(i):
        attempts = []
        start = time()
        while True:
            value = tools.randint(2, i + 100)
            if is_even(value):
                break

            # if len(attempts) > _iter:
            #     break
            attempts.append(value)

        return [i, time() - start, len(attempts), len(attempts) - len(set(attempts)), value]

    data = tools.run_test(
        experiment, _iter, "Even Find Randint Experimentation")
    tools.save_csv(header, data, 'even_randint_data')


#################################################################
#                                                               #
#                  Even Find DSL                                #
#                                                               #
#################################################################
def even_find_dsl(_iter=10000):

    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']

    IsEven = FunctionalConstraint(is_even)

    def experiment(size):
        config.attempts = []
        d = Domain[int](min=2, max=size + 100) | (lambda x: IsEven(x))

        start = time()
        value, _ = d. get_sample()
        return [size, time() - start, len(config.attempts), len(config.attempts) - len(set(config.attempts)), value]

    data = tools.run_test(experiment, _iter, "Even Find DSL Experimentation")
    tools.save_csv(header, data, 'even_dsl_data')


#################################################################
#                                                               #
#                  Even Find Trap                               #
#                                                               #
#################################################################
def even_find_trap(_iter=10000):
    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']
    sampler = UniformSampler()

    def experiment(i):
        attempts = []
        start = time()
        domain = NaturalDomain(2, i + 100)
        while True:
            value = domain.get_sample(sampler)
            if is_even(value):
                break

            domain = domain != value
            attempts.append(value)

        return [i, time() - start, len(attempts), len(attempts) - len(set(attempts)), value]

    data = tools.run_test(
        experiment, _iter, "Even Find Trap Experimentation")
    tools.save_csv(header, data, 'even_trap_data')


#################################################################
#                                                               #
#                  Even Find Trap  Plus                         #
#                                                               #
#################################################################
def even_find_trap_plus(_iter=10000):
    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']
    sampler = UniformSampler()
    domain = NaturalDomain(2, 2)

    def experiment(i):
        nonlocal domain
        attempts = []
        start = time()
        while True:
            domain.extend(i+100)
            value = domain.get_sample(sampler)
            if is_even(value):
                break

            domain = domain != value
            attempts.append(value)

        return [i, time() - start, len(attempts), len(attempts) - len(set(attempts)), value]
    data = tools.run_test(
        experiment, _iter, "Even Find Trap Plus Experimentation")
    tools.save_csv(header, data, 'even_trap_plus_data')

################################################################
#                                                               #
#                  Even Find Randint Fixed                      #
#                                                               #
#################################################################


def even_find_randint_fixed(_iter=10000):

    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']

    def experiment(i):
        attempts = []
        start = time()
        while True:
            value = tools.randint(2, _iter/2)
            if is_even(value):
                break

            # if len(attempts) > _iter:
            #     break
            attempts.append(value)

        return [i, time() - start, len(attempts), len(attempts) - len(set(attempts)), value]

    data = tools.run_test(
        experiment, _iter, "Even Find Randint Fixed Experimentation")
    tools.save_csv(header, data, 'even_randint_fixed_data')

#################################################################
#                                                               #
#                  Even Find DSL Fixed                          #
#                                                               #
#################################################################


def even_find_dsl_fixed(_iter=10000):

    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']

    IsEven = FunctionalConstraint(is_even)
    d = Domain[int](min=2, max=_iter/2) | (lambda x: IsEven(x))

    def experiment(size):
        config.attempts = []

        start = time()
        value, _ = d. get_sample()
        return [size, time() - start, len(config.attempts), len(config.attempts) - len(set(config.attempts)), value]

    data = tools.run_test(
        experiment, _iter, "Even Find DSL Fixed Experimentation")
    tools.save_csv(header, data, 'even_dsl_fixed_data')


#################################################################
#                                                               #
#                  Even Find fixed limits                       #
#                                                               #
#################################################################
def even_find_fixed_limits(_iter=10000):

    header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']
    sampler = UniformSampler()
    domain = NaturalDomain(2, _iter/2)

    def experiment(i):
        nonlocal domain
        attempts = []
        start = time()
        while True:
            value = domain.get_sample(sampler)
            if is_even(value):
                break

            domain = domain != value
            attempts.append(value)

        return [i, time() - start, len(attempts), len(attempts) - len(set(attempts)), value]

    data = tools.run_test(
        experiment, _iter, "Even Find Fixed Limits Experimentation")
    tools.save_csv(header, data, 'even_fixed_data')
