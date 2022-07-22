import imp
from samplers.abstract_def import Sampler
from random import random

class ContinueNormalDistributeSampler(Sampler):
    def get_random_value(self, domain):
        return (domain[1] - domain[0]) * random() + domain[0]

class NaturalNormalDistributeSampler(Sampler):
    def get_random_value(self, domain):
        value = (domain[1] - domain[0]) * random() + domain[0]
        decimal = int(value)
        return int(value) if decimal <= 0.5 else int(value) + 1
