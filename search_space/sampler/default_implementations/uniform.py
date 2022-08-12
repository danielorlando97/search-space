from random import uniform
from search_space.sampler import distribution, Sampler
from search_space.sampler.distribution_names import UNIFORM


@distribution(UNIFORM)
class UniformSampler(Sampler):
    def generate_random_value(self, domain):
        a, b = domain
        return uniform(a, b)
