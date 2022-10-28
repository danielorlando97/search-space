# %%
import csv
from time import time
import matplotlib.pyplot as plt
from search_space.dsl import Domain
from search_space.spaces import FunctionalConstraint
from search_space.context_manager import SearchSpaceConfig
from search_space.utils.infinity import oo
import random


config = SearchSpaceConfig()
config.replay_nums = oo

# %%
print("Simple Set Experimentation")
a, b, _iter = 0, 10000, 9500
header = ['iter_num', 'time', 'attempts']
data = []


def experiment(i):
    result = []
    attempts = 0
    for _ in range(i):
        value = random.randint(a, b)
        while value in result:
            attempts += 1
            value = random.randint(a, b)

            # if attempts > _iter:
            #     break

        result.append(value)

    assert len(result) == len(set(result))
    return attempts


for i in range(_iter):
    print(f'=================== {i} ======================', end='\r')
    start = time()
    attempt = experiment(i)
    result = time() - start

    data.append([i, result, attempt])


with open('experimentation/csv/simple_set.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)


# %%

print("System Set Experimentation")
a, b, _iter = 0, 10000, 9500
header = ['iter_num', 'time', 'attempts']
data = []


def experiment(size):
    d = Domain[int][size](min=a, max=b) | (lambda x, i: x[i] != x[0: i-1])
    config.attempts = []

    def f():
        value, _ = d. get_sample()
        # assert len(value) == len(set(value)), value
        return len(config.attempts)
    return f


for i in range(_iter):
    print(f'=================== {i} ======================', end='\r')

    f = experiment(i)
    start = time()
    attempt = f()
    result = time() - start

    data.append([i, result, attempt])

with open('experimentation/csv/system_set.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)

# %%

print("Simple Even Experimentation")
_iter = 10000
header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']
data = []


def is_even(x: int):
    for i in range(2, x//2 + 1):
        if x % i == 0:
            return False
    return True


def experiment(i):
    attempts = []
    while True:
        value = random.randint(2, i + 100)
        if is_even(value):
            break

        # if len(attempts) > _iter:
        #     break
        attempts.append(value)

    return attempts, value


for i in range(_iter):
    print(f'=================== {i} ======================', end='\r')

    start = time()
    attempt, value = experiment(i)
    result = time() - start

    data.append([i, result, len(attempt), len(
        attempt) - len(set(attempt)), value])

with open('experimentation/csv/simple_even.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)

# %%


print("System Even Experimentation")
_iter = 10000
header = ['iter_num', 'time', 'attempts', 'value_repetition', 'value']
data = []

IsEven = FunctionalConstraint(is_even)


def experiment(size):
    config.attempts = []
    d = Domain[int](min=2, max=size + 100) | (lambda x: IsEven(x))

    def f():
        value, _ = d. get_sample()
        return config.attempts, value
    return f


for i in range(_iter):
    print(f'=================== {i} ======================', end='\r')

    f = experiment(i)
    start = time()
    attempt, value = f()
    result = time() - start

    data.append([i, result, len(attempt), len(
        attempt) - len(set(attempt)), value])

with open('experimentation/csv/system_even.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    writer.writerows(data)
