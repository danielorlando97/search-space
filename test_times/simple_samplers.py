from search_space.dsl import RandomValue, Domain
from .print_lines import plot_time_line
from random import randint


def simple_sample_test(a, b):
    print("Init Simple Test")

    def dsl(): return RandomValue[int](min=a, max=b)

    def best(): return randint(a, b)

    d = Domain[int](min=a, max=b)
    def domain(): return d.get_sample()[0]

    plot_time_line(dsl, best, domain)
