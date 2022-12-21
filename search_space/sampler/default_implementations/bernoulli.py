from random import uniform
from search_space.sampler import Sampler, distribution
from search_space.sampler.distribution_names import UNIFORM_BERNOULLI


@distribution(UNIFORM_BERNOULLI)
class UniformBernoulliSampler(Sampler):
    def generate_random_value(self, domain):
        r = uniform(0, 1)
        return domain[int(r / (1/len(domain)))]
