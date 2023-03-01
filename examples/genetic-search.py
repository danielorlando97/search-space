# %%
from search_space.dsl import Domain
from search_space.spaces import FunctionalConstraint
from search_space.functions.list import Map, Sum
from typing import List
import random

# For having a good folder distribution we add the following two lines
# to add the previous path and to can look the main library
import sys
sys.path.append('../')

# %%

# This project was created, because there were a lot of expressive limitations
# to describe search spaces. When we develop a solution of some search problems
# we have to implement our sampler and it was our description of our search space.
# But this's a very bad way to describe and document our code.

# AutoML systems are the most usually place where we want to describe our search space.
# They also have some problems to describe them. All of their syntax to describe them
# are very influencing by the machine learning domain, because their creators have never thought
# that this descriptions like a single component of this systems, a component that someone can use
# for other research or implementation when he need describe his search space.

# This project has tried to solve all of those problems and made a tools to describe every
# search space as expressive and simply way. In this example we're going to compare the older way
# to solve one search problems to the way that we propose it.

# We're going to use the genetic heuristic to solve the bag problems. The bag problem is a very
# famous NP-hard problems. There are a collection of items and each of them has its weight and
# its prices.


class BagItem:
    WeightDomain = Domain[float](min=0, max=100)
    PriceDomain = Domain[float](min=1, max=50)

    def __init__(self, w: float = WeightDomain, p: float = PriceDomain) -> None:
        self.w, self.p = w, p

# There is also a bag to put these items, but the bag has less capacity than the sum of
# all of items. So, we have to find the way to choose the more economic items for having the bag with
# more possible value


class BagProblem:
    ItemsLenDomain = Domain[int](min=5, max=20)
    ItemsDomain = Domain[BagItem][ItemsLenDomain]()

    WeightDomain = Domain[float](min=0) | (
        lambda x, items=ItemsDomain: x < Sum(Map(items, lambda item: item.w))
    )

    def __init__(self, w: float = WeightDomain, items: List[BagItem] = ItemsDomain) -> None:
        self.w, self.items = w, items

# %%

# These two class will be our description about our problems. This describe is simple,
# declarative and very expressive. Specially, if we compare it with the following example,
# it show the imperative implementation of the sample random space.


def random_bag_problem():
    items = []

    for _ in range(random.randint(5, 20)):
        items.append((
            random.uniform(0, 100),
            random.uniform(1, 50)
        ))

    w = random.uniform(0, sum(map(lambda x: x[0], items)))
    return w, items

# This last version is more simple to implement and we understand it, but it isn't expressive
# because you need understand the programming logic to understand the structure of the random
# space that we want to describe and generate.

# In addition, this version isn't extensible, we cannot change our form to get random number
# without refactoring our sampler. However, we're using a very simple space when to be
# extensible and modular it doesn't matter. But for example in case like AutoML problems
# with have to describe the space of all of machine learning tools, this will be a very hard
# problem if we want to describe it as imperative way.


# %%

# How we have said the bag problem is a NP-hard problem, its search space is so big how to
# iterate for all of possible solution. For that reason we need an heuristic to search
# optimal answer. For arriving it faster we can explore only into the set of feasible solutions.
# We can do this as building and declarative way.


@FunctionalConstraint
def ComputingCurrentCapacity(w: float, items: List[BagItem], current_counts: List[float]):
    current_w = sum([
        count * item.w for count, item in zip(current_counts, items)
    ])

    return (w - current_w) / items[len(current_counts)].w


class BagSolution(BagProblem):
    SolutionDomain = Domain[int][BagProblem.ItemsLenDomain] | (
        lambda x, i,
        w=BagProblem.WeightDomain,
        items=BagProblem.ItemsDomain: (
            # x[i] < ComputingCurrentCapacity(w, items, x[:i - 1])
            x[i] < ComputingCurrentCapacity(w, items, x[:i])
        )
    )

    def validate_solution(self, solution: List[int] = SolutionDomain):
        price = sum([
            item.p * count for item, count in zip(self.items, solution)
        ])
        weight = sum([
            item.w * count for item, count in zip(self.items, solution)
        ])

        assert self.w >= weight
        return price, solution

# This is also clear, each step of the solution building we check how much weight
# we have already and we take how many unit of this item how much capacity we have yet.
# Of course the validate_solution can be smaller that this example but we try to show
# its efficiency

# %%

# Obviously, we can implement this sampler as imperative way


def sample_solution(w, items):
    solution = [0] * len(items)
    w_temp = 0

    for i in range(len(items)):
        top_choice = (w - w_temp) / items[i][0]
        solution[i] = random.randint(0, top_choice)

    price = sum([
        item[1] * count for item, count in zip(items, solution)
    ])

    return price, solution

# %%

# We can show how our library can be part of a genetic algorithm we are going to forget the
# imperative problem random and only we are going to use our SearchSpace as problem sampler.
# But we are going to use the imperative sampler solution for comparing the results. For that
# we are going to need the following connectors


def imperative_sampler_solution(problem: BagProblem):
    return sample_solution(problem.w, [(item.w, item.p) for item in problem.items])


def declarative_sampler_solution(problem: BagSolution):
    return problem.validate_solution()


# %%

# ## Genetic Algorithm

# A genetic algorithm is an heuristic to explore some search space. It is composed by
# a population, a selection function and  a mutably function or crossing function. In this
# case we are going to defined both of them. We also need a validation function, and in the case
# where we will use the description by our library this function has already defined.

def mutably_op(solution):
    return [[count + (i == j) for j, count in enumerate(solution)] for i in range(len(solution))]


def genetic_search(
    problem: BagSolution,
    sampler_solution,
    mutably_op=None,
    crossing_op=None,
    population_size=50,
    generation_limits=100,
    faster_stop=True,
):
    population = []
    for _ in range(population_size):
        _, s = sampler_solution(problem)
        population.append(s)

    optimal = 0
    the_solution = None
    for i in range(generation_limits):
        news = [item for item in generation_limits]

        if mutably_op:

            for solution in population:
                news.extend(mutably_op(solution))

        if crossing_op:

            for i in range(0, len(population)-1):

                news.extend(crossing_op(
                    population[i], population[i+1]
                ))

        values = []
        for i, solution in enumerate(news):
            price, _ = problem.validate_solution(solution)
            values.append(i, price)

        values.sort(key=lambda x: x[0])

        if faster_stop and optimal >= values[0][1]:
            break
        else:
            optimal, the_solution = values[0][1], population[values[0][0]]

        population = [population[i] for i, _ in values]

    return optimal, the_solution


# # Testing

# %%
space = Domain[BagSolution]()
problem, _ = space.get_sample()

# %%
value, solution = genetic_search(
    problem=problem,
    sampler_solution=declarative_sampler_solution,
    mutably_op=mutably_op,
    generation_limits=10
)

# %%
