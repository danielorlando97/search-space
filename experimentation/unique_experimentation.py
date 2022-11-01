# %%
import csv
from time import time
import matplotlib.pyplot as plt
from search_space.dsl import Domain
from search_space.spaces import FunctionalConstraint
from search_space.context_manager import SearchSpaceConfig
from search_space.utils.infinity import oo
import random
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
def set_randint(_iter=9500):
    a, b = 0, _iter + 500
    header = ['iter_num', 'time', 'attempts']

    def experiment(i):

        result = []
        attempts = 0
        start = time()
        for _ in range(i):
            value = random.randint(a, b)
            while value in result:
                attempts += 1
                value = random.randint(a, b)

                # if attempts > _iter:
                #     break

            result.append(value)

        return [i, time() - start, attempts]

    data = tools.run_test(experiment, _iter, "Set Randint Experimentation")
    tools.save_csv(header, data, 'set_randint_data')


#################################################################
#                                                               #
#                  Set DSL                                      #
#                                                               #
#################################################################
def dsl_set(_iter=9500):

    a, b = 0, _iter + 500
    header = ['iter_num', 'time', 'attempts']
    data = []

    def experiment(size):
        d = Domain[int][size](min=a, max=b) | (lambda x, i: x[i] != x[0: i])
        config.attempts = []

        start = time()
        _ = d. get_sample()

        return [size, time() - start, len(config.attempts)]

    data = tools.run_test(experiment, _iter, "Set DSL Experimentation")
    tools.save_csv(header, data, 'set_dsl_data')


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
            value = random.randint(2, i + 100)
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
            value = random.randint(2, _iter)
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
    d = Domain[int](min=2, max=_iter) | (lambda x: IsEven(x))

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
    domain = NaturalDomain(2, _iter)

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
