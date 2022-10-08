from typing import Generic, Protocol, TypeVar
from search_space.sampler import Sampler

T = TypeVar('T')


class DomainProtocol(Generic[T], Protocol):
    def get_sample(self, sampler: Sampler) -> T:
        pass


class NumeralDomainProtocol(DomainProtocol, Protocol):

    @property
    def min(self):
        pass

    @property
    def max(self):
        pass
