from time import time
import matplotlib.pyplot as plt
from search_space.dsl import RandomValue, Domain
import random

_iter = 10000


def plot_time_line(dsl_line, best_line, domain_line, tittle="Simple Test"):

    _, ax = plt.subplots(figsize=(10, 10))

    ax.set_title(tittle, color='C0')

    points = []
    results = []
    start = time()
    for i in range(_iter):
        print(f'1.{i} ....', end='\r')

        points.append(i)
        dsl_line()
        results.append(time() - start)

    ax.plot(points, results, 'C1',
            label=f'dsl compiling and generate: last time {results[-1]}')

    points = []
    results = []
    start = time()
    for i in range(_iter):
        print(f'2.{i} ....', end='\r')

        points.append(i)
        domain_line()
        results.append(time() - start)

    ax.plot(points, results, 'C3',
            label=f'dsl only generate time: last time {results[-1]}')

    points = []
    results = []
    start = time()
    for i in range(_iter):
        print(f'3.{i} ....', end='\r')

        points.append(i)
        best_line()
        results.append(time() - start)

    ax.plot(points, results, 'C2',
            label=f'natural form: last time {results[-1]}')

    ax.legend()
    plt.savefig(f'{tittle}.png')


a, b, size = -100000, 100000, 100


print("Init int experimentation")
d = Domain[int](min=a, max=b)


def dsl(): return RandomValue[int](min=a, max=b)
def best(): return random.randint(a, b)
def domain(): return d.get_sample()[0]


plot_time_line(dsl, best, domain, "Init int experimentation")

print("Init list of int experimentation")
d = Domain[int][size](min=a, max=b)


def best(): return [random.randint(a, b) for _ in range(size)]
def domain(): return d.get_sample()[0]
def dsl(): return RandomValue[int][size](min=a, max=b)


plot_time_line(dsl, best, domain, "Init list of int experimentation")

print("Init class experimentation")


class A:
    def __init__(
        self,
        a: int = Domain[int](min=a, max=b),
        b: int = Domain[int](min=a, max=b)
    ) -> None:
        self.a, self.b = a, b


d = Domain[A]()


def best(): return A(random.randint(a, b), random.randint(a, b))
def domain(): return d.get_sample()[0]
def dsl(): return RandomValue[A]()


plot_time_line(dsl, best, domain, "Init class experimentation")
