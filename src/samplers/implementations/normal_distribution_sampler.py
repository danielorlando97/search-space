import imp
from samplers.abstract_def import Sampler
from random import random


class ContinueNormalDistributeSampler(Sampler):
    def __init__(self, u, o2) -> None:
        super().__init__()
        self.u = u
        self.o2 = o2

    def get_random_value(self, domain):
        return (domain[1] - domain[0]) * random() + domain[0]


class NaturalNormalDistributeSampler(ContinueNormalDistributeSampler):
    def get_random_value(self, domain):
        value = super().get_random_value(domain)
        decimal = int(value)
        return int(value) if decimal <= 0.5 else int(value) + 1
