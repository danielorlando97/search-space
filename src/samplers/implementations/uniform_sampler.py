from random import uniform
from ..abstract_def import distribution, Sampler


@distribution(name='uniform')
class UniformSampler(Sampler):
    def generate_random_value(self, domain):
        a, b = domain
        return uniform(a, b)
