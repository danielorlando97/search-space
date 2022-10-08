from copy import copy
from typing import Generic, List, TypeVar
from search_space.spaces.domains.domain_protocol import DomainProtocol
from search_space.sampler import Sampler, SamplerFactory
from search_space.sampler.distribution_names import UNIFORM

T = TypeVar('T')


class BachedDomain(Generic[T]):
    def __init__(self, *domains: List[DomainProtocol[T]]) -> None:
        self.domains: List[DomainProtocol[T]] = domains
        self.sampler_selector: Sampler = SamplerFactory().create_sampler(UNIFORM, self)

    def get_sample(self, sampler: Sampler) -> T:
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
