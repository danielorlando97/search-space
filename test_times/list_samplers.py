from search_space.dsl import RandomValue, Domain
from .print_lines import plot_time_line
from random import randint


def list_sample_test(a, b, size=100):
    print("Init List Test")

    def dsl():
        return RandomValue[int][size](min=a, max=b)

    def best(): return [randint(a, b) for _ in range(size)]

    d = Domain[int][size](min=a, max=b)
    def domain(): return d.get_sample()[0]

    plot_time_line(dsl, best, domain)
