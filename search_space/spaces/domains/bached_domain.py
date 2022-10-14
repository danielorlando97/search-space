from copy import copy
from typing import List
from search_space.spaces.domains.__base__ import Domain
from search_space.sampler import Sampler, SamplerFactory
from search_space.sampler.distribution_names import UNIFORM
from . import __namespace__ as nsp


class BachedDomain(Domain, metaclass=nsp.BachedDomain):
    def __init__(self, *domains: List[Domain]) -> None:
        self.domains: List[Domain] = list(domains)
        self.sampler_selector: Sampler = SamplerFactory().create_sampler(UNIFORM, self)

    def is_invalid(self):
        index = 0
        while index < len(self.domains):

            if self.domains[index].is_invalid():
                self.domains.pop(index)
            else:
                index += 1

        return len(self.domains) == 0

    @property
    def limits(self):
        self.is_invalid()
        return tuple([d.limits for d in self.domains])

    def get_sample(self, sampler: Sampler):
        bache = self.sampler_selector.choice(self.domains)
        return bache.get_sample(sampler)

    def __copy__(self):
        return BachedDomain(*[copy(d) for d in self.domains])

    def _propagation(self, f):
        for d in self.domains:
            f(d)

    def __eq__(self, other):
        self._propagation(lambda x: x == other)
        return self

    def __ne__(self, other):
        self._propagation(lambda x: x != other)
        return self

    def __lt__(self, other):
        self._propagation(lambda x: x < other)
        return self

    def __gt__(self, other):
        self._propagation(lambda x: x > other)
        return self

    def __ge__(self, other):
        self._propagation(lambda x: x >= other)
        return self

    def __le__(self, other):
        self._propagation(lambda x: x <= other)
        return self

    def __or__(self, __o):
        return self.domains.append(__o)

    def __hash__(self) -> int:
        return id(self)
