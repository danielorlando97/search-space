from time import time
from unittest import result
from search_space.dsl import RandomValue, Domain
from search_space.spaces.build_in_spaces import BasicNaturalSearchSpace
from . import tools

#################################################################
#                                                               #
#                  DSL Int vs Randint                           #
#                                                               #
#################################################################


def dsl_vs_randint_int(_iter=10000):
    a, b = -100000, 100000
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
        _ = tools.randint(a, b)
        result.append(time() - start)

        return result

    data = tools.run_test(
        experiment, _iter, "Generate Int Time Experimentation")
    tools.save_csv(header, data, 'int_times')

#################################################################
#                                                               #
#                  Choice                                       #
#                                                               #
#################################################################


def dsl_choice(_iter=10000):
    options = [str(i) for i in range(1000)]
    space = Domain[str](options=options)
    header = ['index', 'time_dsl', 'time_generation', 'time_random']

    def experiment(i):
        result = [i]

        # Total DSL Time
        start = time()
        _ = RandomValue[str](options=options)
        result.append(time() - start)

        # DSL Generate Time
        start = time()
        _ = space.get_sample()[0]
        result.append(time() - start)

        start = time()
        _ = tools.choice(options)
        result.append(time() - start)

        return result

    data = tools.run_test(
        experiment, _iter, "Choice Time Experimentation")
    tools.save_csv(header, data, 'choice_times')

#################################################################
#                                                               #
#          DSL List[Int] vs [Randint]                           #
#                                                               #
#################################################################


def dsl_vs_randint_list_int(_iter=10000):

    a, b, size = -100000, 100000, 1000
    space = Domain[int][size](min=a, max=b)
    d = BasicNaturalSearchSpace(min=a, max=b)
    header = ['index', 'time_dsl', 'time_generation',
              'time_random', 'time_generation_single']

    def experiment(i):
        result = [i]

        # Total DSL Time
        start = time()
        _ = RandomValue[int][size](min=a, max=b)
        result.append(time() - start)

        # DSL Generate Time
        start = time()
        _ = space.get_sample()
        result.append(time() - start)

        start = time()
        _ = [tools.randint(a, b) for _ in range(size)]
        result.append(time() - start)

        start = time()
        _ = [d.get_sample()[0] for _ in range(size)]
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
    header = ['index', 'time_dsl', 'time_generation',
              'time_random', 'time_generation_single']
    d = BasicNaturalSearchSpace(min=a, max=b)

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
        _ = A(tools.randint(a, b), tools.randint(a, b))
        result.append(time() - start)

        start = time()
        _ = A(d.get_sample()[0], d.get_sample()[0])
        result.append(time() - start)

        return result

    data = tools.run_test(
        experiment, _iter, "Generate Class Time Experimentation")
    tools.save_csv(header, data, 'class_times')
