from time import time
from unittest import result
from search_space.dsl import RandomValue, Domain
import random
from . import tools

#################################################################
#                                                               #
#                  DSL Int vs Randint                           #
#                                                               #
#################################################################


def dsl_vs_randint_int(_iter=10000):
    a, b, _iter = -100000, 100000, 10000
    space = Domain[int](min=a, max=b)
    header = ['index', 'time_dsl', 'time_generation', 'time_random']

    def experiment(i):
        result = [i]

        # Total DSL Time
        start = time()
        _ = RandomValue[int](min=a, max=b)
        result.append(time() - start)

        # DSL Generate Time
        start = time()
        _ = space.get_sample()[0]
        result.append(time() - start)

        start = time()
        _ = random.randint(a, b)
        result.append(time() - start)

        return result

    data = tools.run_test(
        experiment, _iter, "Generate Int Time Experimentation")
    tools.save_csv(header, data, 'int_times')

#################################################################
#                                                               #
#          DSL List[Int] vs [Randint]                           #
#                                                               #
#################################################################


def dsl_vs_randint_list_int(_iter=10000):

    a, b, size = -100000, 100000, 1000
    space = Domain[int][size](min=a, max=b)
    header = ['index', 'time_dsl', 'time_generation', 'time_random']

    def experiment(i):
        result = [i]

        # Total DSL Time
        start = time()
        _ = RandomValue[int][size](min=a, max=b)
        result.append(time() - start)

        # DSL Generate Time
        start = time()
        _ = space.get_sample()[0]
        result.append(time() - start)

        start = time()
        _ = [random.randint(a, b) for _ in range(size)]
        result.append(time() - start)

        return result

    data = tools.run_test(
        experiment, _iter, "Generate List[Int] Time Experimentation")
    tools.save_csv(header, data, 'list_times')


#################################################################
#                                                               #
#          DSL Class vs Class(Randint)                          #
#                                                               #
#################################################################
def dsl_vs_randint_class(_iter=10000):

    a, b = -100000, 100000
    header = ['index', 'time_dsl', 'time_generation', 'time_random']

    class A:
        def __init__(
            self,
            a: int = Domain[int](min=a, max=b),
            b: int = Domain[int](min=a, max=b)
        ) -> None:
            self.a, self.b = a, b

    space = Domain[A]()

    def experiment(i):
        result = [i]

        # Total DSL Time
        start = time()
        _ = RandomValue[A]()
        result.append(time() - start)

        # DSL Generate Time
        start = time()
        _ = space.get_sample()[0]
        result.append(time() - start)

        start = time()
        _ = A(random.randint(a, b), random.randint(a, b))
        result.append(time() - start)

        return result

    data = tools.run_test(
        experiment, _iter, "Generate Class Time Experimentation")
    tools.save_csv(header, data, 'class_times')
